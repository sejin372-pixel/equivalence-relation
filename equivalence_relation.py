import copy

# 대상 집합 A = {1, 2, 3, 4, 5}
SET_A = [1, 2, 3, 4, 5]
N = len(SET_A)


# [조건 1] 관계 행렬 입력 및 출력 기능

def input_relation_matrix():
    """5x5 크기의 정방행렬을 행 단위로 입력받아 2차원 리스트로 반환"""
    print(f"집합 A = {SET_A} 에 대한 5x5 관계 행렬을 행 단위로 입력하세요 (0 또는 1, 공백 구분):")
    matrix = []
    for i in range(N):
        while True:
            try:
                row = list(map(int, input(f"{i + 1}행 입력: ").strip().split()))
                if len(row) != N or any(val not in (0, 1) for val in row):
                    print(f"[오류] 0과 1로 이루어진 {N}개의 정수를 공백으로 구분해 다시 입력하세요.")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("[오류] 올바른 숫자를 입력하세요.")
    return matrix


def print_matrix(matrix, title="관계 행렬"):
    """2차원 리스트 형태의 관계 행렬을 보기 좋게 출력"""
    print(f"\n[{title}]")
    for row in matrix:
        print(" ".join(map(str, row)))


# [조건 2] 동치 관계 판별 기능 (반사, 대칭, 추이)

def is_reflexive(matrix):
    """반사 관계 판별: 모든 i에 대해 M[i][i] == 1"""
    for i in range(N):
        if matrix[i][i] != 1:
            return False
    return True


def is_symmetric(matrix):
    """대칭 관계 판별: 모든 i, j에 대해 M[i][j] == M[j][i]"""
    for i in range(N):
        for j in range(i + 1, N):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


def is_transitive(matrix):
    """추이 관계 판별: M[i][k] == 1 이고 M[k][j] == 1 이면 M[i][j] == 1"""
    for i in range(N):
        for k in range(N):
            if matrix[i][k] == 1:
                for j in range(N):
                    if matrix[k][j] == 1 and matrix[i][j] != 1:
                        return False
    return True


# [추가 기능] 관계 위배 반례(Counterexample) 자동 추적 기능

def find_reflexive_counterexamples(matrix):
    """반사 관계 위배 반례 추적: (a, a)가 관계에 포함되지 않은 원소 쌍 반환"""
    counterexamples = []
    for i in range(N):
        if matrix[i][i] != 1:
            counterexamples.append((SET_A[i], SET_A[i]))
    return counterexamples


def find_symmetric_counterexamples(matrix):
    """대칭 관계 위배 반례 추적: (a, b)는 존재하지만 (b, a)가 없는 원소 쌍 반환"""
    counterexamples = []
    for i in range(N):
        for j in range(N):
            if i != j and matrix[i][j] == 1 and matrix[j][i] == 0:
                counterexamples.append(((SET_A[i], SET_A[j]), (SET_A[j], SET_A[i])))
    return counterexamples


def find_transitive_counterexamples(matrix):
    """추이 관계 위배 반례 추적: (a, b)와 (b, c)는 존재하지만 (a, c)가 없는 원소 쌍 반환"""
    counterexamples = []
    for i in range(N):
        for k in range(N):
            if matrix[i][k] == 1:
                for j in range(N):
                    if matrix[k][j] == 1 and matrix[i][j] != 1:
                        counterexamples.append(
                            ((SET_A[i], SET_A[k]), (SET_A[k], SET_A[j]), (SET_A[i], SET_A[j]))
                        )
    return counterexamples


def print_counterexamples(matrix, ref, sym, tra):
    """위배된 성질에 대한 구체적인 반례를 추적하여 출력"""
    if ref and sym and tra:
        return

    print("\n[추가 기능] 관계 성질 위배 반례(Counterexample) 분석:")
    if not ref:
        ref_ce = find_reflexive_counterexamples(matrix)
        ce_str = ", ".join(f"{pair} ∉ R" for pair in ref_ce)
        print(f"  - 반사 위배 반례 ({len(ref_ce)}건): {ce_str}")

    if not sym:
        sym_ce = find_symmetric_counterexamples(matrix)
        ce_str = ", ".join(f"{p1} ∈ R 이지만 {p2} ∉ R" for p1, p2 in sym_ce)
        print(f"  - 대칭 위배 반례 ({len(sym_ce)}건): {ce_str}")

    if not tra:
        tra_ce = find_transitive_counterexamples(matrix)
        ce_str = ", ".join(f"{p1}, {p2} ∈ R 이지만 {p3} ∉ R" for p1, p2, p3 in tra_ce)
        print(f"  - 추이 위배 반례 ({len(tra_ce)}건): {ce_str}")


def check_equivalence_relation(matrix):
    """반사, 대칭, 추이 성질을 판별하고 동치 관계 여부 및 위배 반례를 출력"""
    ref = is_reflexive(matrix)
    sym = is_symmetric(matrix)
    tra = is_transitive(matrix)

    print("\n--- 관계 성질 판별 결과 ---")
    print(f"1. 반사 관계 (Reflexive) : {'만족 (True)' if ref else '불만족 (False)'}")
    print(f"2. 대칭 관계 (Symmetric) : {'만족 (True)' if sym else '불만족 (False)'}")
    print(f"3. 추이 관계 (Transitive): {'만족 (True)' if tra else '불만족 (False)'}")

    # 불만족 성질이 있을 경우 반례 자동 추적 및 출력
    print_counterexamples(matrix, ref, sym, tra)

    is_eq = ref and sym and tra
    if is_eq:
        print("=> 판별 결과: 이 관계는 [동치 관계]입니다.")
    else:
        print("=> 판별 결과: 이 관계는 [동치 관계가 아닙니다].")

    return is_eq, ref, sym, tra

# [조건 3] 동치 관계일 경우 동치류 출력 기능

def get_equivalence_class(matrix, element_idx):
    """특정 원소(인덱스)에 대한 동치류 집합 반환"""
    return [SET_A[j] for j in range(N) if matrix[element_idx][j] == 1]


def print_equivalence_classes(matrix):
    """집합 A의 각 원소에 대한 동치류를 모두 출력"""
    print("\n--- 각 원소의 동치류 (Equivalence Classes) ---")
    for i in range(N):
        eq_class = get_equivalence_class(matrix, i)
        eq_str = ", ".join(map(str, eq_class))
        print(f"[{SET_A[i]}] = {{{eq_str}}}")


# [조건 4] 폐포(Closure) 구현 및 재판별 기능

def reflexive_closure(matrix):
    """반사 폐포 생성"""
    closure = copy.deepcopy(matrix)
    for i in range(N):
        closure[i][i] = 1
    return closure

def symmetric_closure(matrix):
    """대칭 폐포 생성"""
    closure = copy.deepcopy(matrix)
    for i in range(N):
        for j in range(N):
            if closure[i][j] == 1 or closure[j][i] == 1:
                closure[i][j] = 1
                closure[j][i] = 1
    return closure

def transitive_closure(matrix):
    """추이 폐포 생성 (Warshall 알고리즘)"""
    closure = copy.deepcopy(matrix)
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if closure[i][k] == 1 and closure[k][j] == 1:
                    closure[i][j] = 1
    return closure


def handle_closures(matrix, ref, sym, tra):
    """만족하지 않는 성질에 대해 각각의 폐포 변환 전/후 출력 및 동치 관계 재판별"""
    print("\n==============================================")
    print("동치 관계가 아니므로 만족하지 않는 성질의 폐포를 생성합니다.")
    print("==============================================")

    # 1. 반사 관계가 아닐 경우 반사 폐포 적용
    if not ref:
        print("\n>>> [반사 폐포(Reflexive Closure) 변환]")
        print_matrix(matrix, "변환 전 행렬")
        r_mat = reflexive_closure(matrix)
        print_matrix(r_mat, "변환 후 행렬 (반사 폐포)")
        is_eq, _, _, _ = check_equivalence_relation(r_mat)
        if is_eq:
            print_equivalence_classes(r_mat)

    # 2. 대칭 관계가 아닐 경우 대칭 폐포 적용
    if not sym:
        print("\n>>> [대칭 폐포(Symmetric Closure) 변환]")
        print_matrix(matrix, "변환 전 행렬")
        s_mat = symmetric_closure(matrix)
        print_matrix(s_mat, "변환 후 행렬 (대칭 폐포)")
        is_eq, _, _, _ = check_equivalence_relation(s_mat)
        if is_eq:
            print_equivalence_classes(s_mat)

    # 3. 추이 관계가 아닐 경우 추이 폐포 적용
    if not tra:
        print("\n>>> [추이 폐포(Transitive Closure) 변환]")
        print_matrix(matrix, "변환 전 행렬")
        t_mat = transitive_closure(matrix)
        print_matrix(t_mat, "변환 후 행렬 (추이 폐포)")
        is_eq, _, _, _ = check_equivalence_relation(t_mat)
        if is_eq:
            print_equivalence_classes(t_mat)

    # 4. 두 가지 이상의 성질이 동시에 위배된 경우, 순차 적용(반사->대칭->추이)으로 최종 동치 폐포 도출
    violated_count = [ref, sym, tra].count(False)
    if violated_count >= 2:
        print("\n>>> [복합 성질 위배: 반사 -> 대칭 -> 추이 폐포 순차 적용]")
        print_matrix(matrix, "최초 입력 행렬")
        eq_mat = transitive_closure(symmetric_closure(reflexive_closure(matrix)))
        print_matrix(eq_mat, "최종 동치 폐포 변환 후 행렬")
        is_eq, _, _, _ = check_equivalence_relation(eq_mat)
        if is_eq:
            print_equivalence_classes(eq_mat)


def main():
    relation_matrix = input_relation_matrix()
    print_matrix(relation_matrix, "입력된 관계 행렬")

    is_eq, ref, sym, tra = check_equivalence_relation(relation_matrix)

    if is_eq:
        print_equivalence_classes(relation_matrix)
    else:
        handle_closures(relation_matrix, ref, sym, tra)


if __name__ == "__main__":
    main()
