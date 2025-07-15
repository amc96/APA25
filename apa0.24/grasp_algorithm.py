import numpy as np
import random
from typing import List, Tuple, Callable, Optional

class GRASPOptimizer:
    """
    GRASP (Greedy Randomized Adaptive Search Procedure) optimizer for 
    animal breeding optimization to minimize coancestry working directly on crossing matrix.
    """
    
    def __init__(self, coancestry_matrix: np.ndarray, max_iterations: int = 200, 
                 alpha: float = 0.3, local_search_iterations: int = 30, 
                 pair_names: list = None):
        """
        Initialize GRASP optimizer.
        
        Args:
            coancestry_matrix: Square matrix of coancestry values between all crossing pairs
            max_iterations: Maximum number of GRASP iterations
            alpha: Greedy parameter (0 = pure greedy, 1 = pure random)
            local_search_iterations: Number of local search iterations
            pair_names: List of pair names corresponding to matrix indices
        """
        self.coancestry_matrix = coancestry_matrix
        self.matrix_size = coancestry_matrix.shape[0]
        self.max_iterations = max_iterations
        self.alpha = alpha
        self.local_search_iterations = local_search_iterations
        self.pair_names = pair_names if pair_names else [f'P{i+1}' for i in range(self.matrix_size)]
        
        # For tracking convergence
        self.iteration_costs = []
        self.best_solution = None
        self.best_cost = float('inf')
        self.best_crossings = []
    
    def calculate_total_cost(self, selected_crossings: List[int]) -> float:
        """
        Calculate the total coancestry cost for selected crossings from the matrix.
        
        Args:
            selected_crossings: List of indices representing selected crossing pairs
            
        Returns:
            Total coancestry cost (sum of selected coancestry coefficients)
        """
        total_cost = 0.0
        
        # Somar os coeficientes de coancestralidade dos cruzamentos selecionados
        for crossing_idx in selected_crossings:
            # Usar apenas a diagonal inferior para evitar duplicatas
            row = crossing_idx // self.matrix_size
            col = crossing_idx % self.matrix_size
            
            # Só considerar se não for a diagonal principal (mesmo animal)
            if row != col:
                total_cost += self.coancestry_matrix[row, col]
        
        return total_cost
    
    def calculate_crossing_matrix_cost(self, solution_matrix: np.ndarray) -> float:
        """
        Calculate cost directly from a solution matrix where 1 indicates selected crossings.
        
        Args:
            solution_matrix: Binary matrix indicating selected crossings
            
        Returns:
            Total coancestry cost
        """
        total_cost = 0.0
        
        # Somar apenas os valores onde a matriz solução indica 1
        for i in range(self.matrix_size):
            for j in range(i + 1, self.matrix_size):  # Usar apenas triangular superior
                if solution_matrix[i, j] == 1:
                    total_cost += self.coancestry_matrix[i, j]
        
        return total_cost
    
    def greedy_randomized_construction(self, num_crossings: int = None) -> List[Tuple[int, int]]:
        """
        Construct a solution using greedy randomized construction working on crossing matrix.
        Optimized version with pre-sorted crossings and improved randomization.
        
        Args:
            num_crossings: Number of crossings to select (default: matrix_size // 3)
            
        Returns:
            A solution as a list of crossing pairs (row, col)
        """
        if num_crossings is None:
            num_crossings = max(3, min(20, self.matrix_size // 10))  # Limitar ainda mais o número de cruzamentos
        
        solution = []
        used_pairs = set()
        used_animals = set()  # Para evitar sequência de animais
        
        # Pré-calcular todos os cruzamentos possíveis ordenados (cache)
        if not hasattr(self, '_sorted_crossings'):
            all_crossings = []
            for i in range(self.matrix_size):
                for j in range(i + 1, self.matrix_size):
                    all_crossings.append((i, j, self.coancestry_matrix[i, j]))
            
            # Ordenar por coeficiente de coancestralidade (menor é melhor)
            all_crossings.sort(key=lambda x: x[2])
            self._sorted_crossings = all_crossings
        
        # Embaralhar os candidatos para evitar sequência
        candidate_pool = self._sorted_crossings.copy()
        random.shuffle(candidate_pool)
        
        # Limitar número de candidatos baseado no número de iterações para balance performance/qualidade
        if self.max_iterations > 500:
            max_candidates = min(100, len(candidate_pool))  # Muito menos candidatos para iterações altas
        elif self.max_iterations > 200:
            max_candidates = min(150, len(candidate_pool))  # Menos candidatos para iterações médias
        else:
            max_candidates = min(300, len(candidate_pool))  # Candidatos normais para iterações baixas
        
        candidate_pool = candidate_pool[:max_candidates]
        
        # Reordenar por coancestralidade após embaralhamento
        candidate_pool.sort(key=lambda x: x[2])
        
        for _ in range(min(num_crossings, len(candidate_pool))):
            # Criar lista de candidatos ainda não utilizados
            candidates = []
            for i, j, coef in candidate_pool:
                # Evitar usar animais em sequência ou já utilizados
                if (i, j) not in used_pairs and i not in used_animals and j not in used_animals:
                    candidates.append((i, j, coef))
            
            # Se não há candidatos completamente novos, permitir reutilizar alguns animais
            if not candidates:
                for i, j, coef in candidate_pool:
                    if (i, j) not in used_pairs:
                        candidates.append((i, j, coef))
            
            if not candidates:
                break
            
            # Usar apenas os melhores candidatos para RCL com randomização
            num_rcl_candidates = min(100, len(candidates))
            top_candidates = candidates[:num_rcl_candidates]
            
            # Criar lista restrita de candidatos (RCL) com diversidade
            min_cost = top_candidates[0][2]
            max_cost = top_candidates[-1][2]
            threshold = min_cost + self.alpha * (max_cost - min_cost)
            
            rcl = [(i, j) for i, j, coef in top_candidates if coef <= threshold]
            
            # Adicionar algumas opções aleatórias para diversidade
            if len(rcl) < 10 and len(candidates) > len(rcl):
                additional_candidates = random.sample(candidates[len(rcl):], 
                                                    min(5, len(candidates) - len(rcl)))
                rcl.extend(additional_candidates)
            
            # Selecionar aleatoriamente da RCL
            selected_crossing = random.choice(rcl)
            solution.append(selected_crossing)
            used_pairs.add(selected_crossing)
            
            # Marcar animais como usados por algumas iterações para evitar sequência
            if len(solution) % 3 == 0:  # A cada 3 seleções, limpar alguns animais usados
                used_animals.clear()
            else:
                used_animals.add(selected_crossing[0])
                used_animals.add(selected_crossing[1])
        
        return solution
    
    def local_search(self, solution: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Perform local search to improve the solution working on crossing pairs.
        Optimized version with limited search space and randomization.
        
        Args:
            solution: Current solution as list of crossing pairs
            
        Returns:
            Improved solution
        """
        current_solution = solution.copy()
        current_cost = self.calculate_crossing_cost(current_solution)
        
        improved = True
        iterations = 0
        
        # Pré-calcular todos os cruzamentos possíveis ordenados por coancestralidade
        if not hasattr(self, '_sorted_crossings'):
            all_crossings = []
            for i in range(self.matrix_size):
                for j in range(i + 1, self.matrix_size):
                    all_crossings.append((i, j, self.coancestry_matrix[i, j]))
            
            # Ordenar por coancestralidade (menor primeiro)
            all_crossings.sort(key=lambda x: x[2])
            self._sorted_crossings = all_crossings
        
        # Embaralhar candidatos para evitar padrões sequenciais
        candidate_pool = self._sorted_crossings.copy()
        random.shuffle(candidate_pool)
        
        # Limitar número de candidatos baseado no número de iterações para otimização
        if self.max_iterations > 500:
            max_candidates = min(50, len(candidate_pool))  # Muito menos candidatos para iterações altas
        elif self.max_iterations > 200:
            max_candidates = min(75, len(candidate_pool))  # Candidatos reduzidos
        else:
            max_candidates = min(100, len(candidate_pool))  # Candidatos normais para iterações baixas
        
        top_candidates = candidate_pool[:max_candidates]
        
        # Reordenar por coancestralidade após embaralhamento
        top_candidates.sort(key=lambda x: x[2])
        
        while improved and iterations < self.local_search_iterations:
            improved = False
            iterations += 1
            
            # Embaralhar a ordem de verificação das soluções atuais
            solution_indices = list(range(len(current_solution)))
            random.shuffle(solution_indices)
            
            # Tentar trocar cruzamentos da solução atual por candidatos melhores
            for idx in solution_indices:
                current_crossing = current_solution[idx]
                current_i, current_j = current_crossing
                current_crossing_cost = self.coancestry_matrix[current_i, current_j]
                
                # Embaralhar candidatos para cada verificação
                random.shuffle(top_candidates)
                
                # Tentar substituir por candidatos de baixa coancestralidade
                for new_i, new_j, new_cost in top_candidates:
                    if (new_i, new_j) not in current_solution and new_cost < current_crossing_cost:
                        # Verificar se não cria sequência de animais
                        current_animals = set()
                        for ci, cj in current_solution:
                            if (ci, cj) != current_crossing:
                                current_animals.add(ci)
                                current_animals.add(cj)
                        
                        # Aceitar substituição se não cria muita sobreposição
                        if new_i not in current_animals or new_j not in current_animals:
                            new_solution = current_solution.copy()
                            new_solution[idx] = (new_i, new_j)
                            
                            total_new_cost = self.calculate_crossing_cost(new_solution)
                            
                            if total_new_cost < current_cost:
                                current_solution = new_solution
                                current_cost = total_new_cost
                                improved = True
                                break
                
                if improved:
                    break
        
        return current_solution
    
    def calculate_crossing_cost(self, solution: List[Tuple[int, int]]) -> float:
        """
        Calculate cost for a solution of crossing pairs.
        
        Args:
            solution: List of crossing pairs (row, col)
            
        Returns:
            Total coancestry cost
        """
        total_cost = 0.0
        for i, j in solution:
            total_cost += self.coancestry_matrix[i, j]
        return total_cost
    
    def optimize(self, progress_callback: Optional[Callable] = None, num_crossings: int = None) -> Tuple[List[Tuple[int, int]], float, List[float]]:
        """
        Run the GRASP optimization algorithm working on crossing matrix.
        
        Args:
            progress_callback: Optional callback function for progress updates
            num_crossings: Number of crossings to select in each solution
            
        Returns:
            Tuple of (best_solution, best_cost, iteration_costs)
        """
        self.iteration_costs = []
        self.best_solution = None
        self.best_cost = float('inf')
        self.best_crossings = []
        
        no_improvement_count = 0
        max_no_improvement = min(50, self.max_iterations // 10)  # Convergência antecipada adaptativa
        
        for iteration in range(self.max_iterations):
            # Construction phase - selecionar cruzamentos da matriz
            solution = self.greedy_randomized_construction(num_crossings)
            
            # Local search phase - aplicar com menos frequência para iterações altas
            if self.max_iterations > 500 and iteration % 3 == 0:
                solution = self.local_search(solution)  # Busca local esporádica
            elif self.max_iterations <= 500:
                solution = self.local_search(solution)  # Busca local normal
            
            # Evaluate solution
            cost = self.calculate_crossing_cost(solution)
            
            # Update best solution
            if cost < self.best_cost:
                self.best_cost = cost
                # Diversificar solução antes de salvar
                diversified_solution = self.diversify_solution(solution)
                self.best_solution = diversified_solution.copy()
                self.best_crossings = self.convert_to_crossing_details(diversified_solution)
                no_improvement_count = 0  # Reset contador
            else:
                no_improvement_count += 1
            
            # Track progress
            self.iteration_costs.append(self.best_cost)
            
            # Call progress callback if provided
            if progress_callback:
                progress_callback(iteration + 1, self.best_cost)
            
            # Convergência antecipada se não há melhoria por muitas iterações
            if no_improvement_count >= max_no_improvement:
                break
        
        return self.best_solution, self.best_cost, self.iteration_costs
    
    def convert_to_crossing_details(self, solution: List[Tuple[int, int]]) -> List[dict]:
        """
        Convert solution to detailed crossing information.
        
        Args:
            solution: List of crossing pairs (row, col)
            
        Returns:
            List of dictionaries with crossing details
        """
        crossings = []
        for i, j in solution:
            crossings.append({
                'pair1_idx': i,
                'pair2_idx': j,
                'pair1_name': self.pair_names[i],
                'pair2_name': self.pair_names[j],
                'coancestry': self.coancestry_matrix[i, j]
            })
        
        # Ordenar por coancestralidade (menor primeiro)
        crossings.sort(key=lambda x: x['coancestry'])
        return crossings
    
    def diversify_solution(self, solution: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Diversifica a solução para evitar usar animais em sequência.
        
        Args:
            solution: Solução atual
            
        Returns:
            Solução diversificada
        """
        if len(solution) <= 1:
            return solution
            
        diversified = []
        used_animals = set()
        
        # Primeira passagem: incluir cruzamentos sem animais repetidos
        for crossing in solution:
            i, j = crossing
            if i not in used_animals and j not in used_animals:
                diversified.append(crossing)
                used_animals.add(i)
                used_animals.add(j)
        
        # Segunda passagem: incluir cruzamentos restantes com menor sobreposição
        for crossing in solution:
            if crossing not in diversified:
                i, j = crossing
                overlap = (i in used_animals) + (j in used_animals)
                if overlap <= 1:  # Permitir sobreposição de até 1 animal
                    diversified.append(crossing)
                    used_animals.add(i)
                    used_animals.add(j)
        
        # Se ainda não temos cruzamentos suficientes, incluir os restantes
        if len(diversified) < len(solution) // 2:
            for crossing in solution:
                if crossing not in diversified:
                    diversified.append(crossing)
                    if len(diversified) >= len(solution):
                        break
        
        return diversified
    
    def get_best_crossings_matrix(self) -> np.ndarray:
        """
        Create a matrix highlighting the best crossings found.
        
        Returns:
            Binary matrix where 1 indicates selected crossings
        """
        matrix = np.zeros_like(self.coancestry_matrix)
        
        if self.best_solution:
            for i, j in self.best_solution:
                matrix[i, j] = 1
                matrix[j, i] = 1  # Simetria
        
        return matrix
    
    def get_all_crossings_ranked(self) -> List[dict]:
        """
        Get all possible crossings ranked by coancestry coefficient.
        
        Returns:
            List of all crossings sorted by coancestry (best first)
        """
        all_crossings = []
        
        for i in range(self.matrix_size):
            for j in range(i + 1, self.matrix_size):
                all_crossings.append({
                    'pair1_idx': i,
                    'pair2_idx': j,
                    'pair1_name': self.pair_names[i],
                    'pair2_name': self.pair_names[j],
                    'coancestry': self.coancestry_matrix[i, j],
                    'selected': (i, j) in (self.best_solution or [])
                })
        
        # Ordenar por coancestralidade (menor primeiro)
        all_crossings.sort(key=lambda x: x['coancestry'])
        return all_crossings
    
    def get_solution_statistics(self, solution: List[int]) -> dict:
        """
        Get statistics about a solution.
        
        Args:
            solution: Solution to analyze
            
        Returns:
            Dictionary with solution statistics
        """
        male_usage = {}
        for male_idx in solution:
            male_usage[male_idx] = male_usage.get(male_idx, 0) + 1
        
        coancestry_values = [self.coancestry_matrix[i, solution[i]] for i in range(self.num_females)]
        
        return {
            'total_cost': self.calculate_total_cost(solution),
            'male_usage': male_usage,
            'avg_coancestry': np.mean(coancestry_values),
            'max_coancestry': np.max(coancestry_values),
            'min_coancestry': np.min(coancestry_values),
            'num_unique_males': len(set(solution))
        }
