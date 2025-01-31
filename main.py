from src.use_cases_generator import generate_use_case
from src.test_case_generator import generate_test_case
from src.script_test_case_generator import generate_test_case_script
from src.tools import save_file

def main():
    use_case = generate_use_case()
    print(f'\n{use_case}\n')

    test_case = generate_test_case(use_case)
    print(f'\n{test_case}\n')

    test_case_script = generate_test_case_script(use_case, test_case)
    print(f'\n{test_case_script}\n')

    save_file('tests/test_login.py', test_case_script)

if __name__ == "__main__":
    main()