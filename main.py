from src.use_cases_generator import generate_use_case
from src.test_case_generator import generate_test_case
from src.script_test_case_generator import generate_test_case_script
from src.tools import *

def main():
    use_case_description = input('Digite a descrição do caso de uso: ')

    use_case = generate_use_case(use_case_description, STANDARD_MODEL)
    print(f'\nCaso de uso (não refinado)\n{use_case}\n')

    use_case = generate_use_case(use_case_description, REFINED_MODEL)
    print(f'\nCaso de uso (refinado)\n{use_case}\n')

    """test_case = generate_test_case(use_case)
    print(f'\n{test_case}\n')

    test_case_script = generate_test_case_script(use_case, test_case)
    print(f'\n{test_case_script}\n')

    save_file('tests/test_login.py', test_case_script)"""

if __name__ == "__main__":
    main()