```
python3 -m venv venv
source venv/bin/activate
```


```bash
pip install "Flask[async]"
```

## Freeze

```bash
pip freeze > requirements.txt
```

## Run

```bash
python3 run_worker.py
flask --app run_flask --debug run
```

## Terminate

```bash
temporal workflow terminate --workflow-id=send-email-activity
```