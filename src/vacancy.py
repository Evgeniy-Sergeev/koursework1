class Vacancy:
    __slots__ = ['title', 'url', 'salary', 'description']

    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = self._validate_title(title)
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    @staticmethod
    def _validate_title(title: str) -> str:
        if not title:
            raise ValueError("Title cannot be empty")
        return title

    @staticmethod
    def _validate_salary(salary: str) -> str:
        if salary == 'Зарплата не указана':
            return '0'
        return salary

    def __repr__(self):
        return f"{self.title} ({self.salary}) - {self.url}"

    def __eq__(self, other):
        return self.salary == other.salary

    def __lt__(self, other):
        return self._parse_salary(self.salary) < self._parse_salary(other.salary)

    @staticmethod
    def _parse_salary(salary: str) -> int:
        if salary == '0':
            return 0
        salary_range = salary.replace(' ', '').split('-')
        return int(salary_range[0])
