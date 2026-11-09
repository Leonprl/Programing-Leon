# Programing-Leon

My exercises for the Object Oriented Programming & Design Patterns course (Bachelor AIDAMS, 2nd year).

## Content

| Folder | What's inside |
|---|---|
| `install.sh` | first git workflow exercise (branch + merge) |
| `linux/` | `env_install.sh` - bash script that installs python, pip and jupyter (mac / linux) |
| `oop/` | operator overloading (complex numbers, vectors, matrices...) and inheritance problems |
| `uml/` | class + sequence diagrams for the hospital and ABCD Records exercises (mermaid) |
| `design_patterns/creational/` | Factory (payments), Builder (employee onboarding), Singleton (config manager) |
| `design_patterns/structural/` | Adapter (XML -> JSON reports), Decorator (order pricing) |
| `design_patterns/behavioral/` | Strategy (report formats), Template Method (ETL pipelines) |
| `tests/` | pytest tests |

## Run

```bash
pip install -r requirements.txt
python3 design_patterns/creational/payment_factory.py
pytest
```

For the bash script:

```bash
chmod +x linux/env_install.sh
./linux/env_install.sh --dry-run
```
