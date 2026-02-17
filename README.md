# Health Monitor

Prosty backend w FastAPI do monitorowania serwisów HTTP.

## Co robi aplikacja
- dodaje serwisy do monitorowania,
- ustawia harmonogram pingów,
- zapisuje historię zdarzeń (`UP` / `DOWN`),
- pozwala przeglądać logi.

## Szybki start

### 1) Wejdź do projektu
```bash
cd health_monitor
```

### 2) Utwórz i odpal venv (Linux/macOS)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3) Zainstaluj zależności
```bash
pip install -r requirements.txt
```

### 4) Uruchom API
```bash
uvicorn app.main:app --reload
```

Po starcie:
- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

## Najważniejsze endpointy

### Services
- `POST /services/`
- `GET /services/`
- `GET /services/{service_id}`
- `DELETE /services/{service_id}`

### Schedules
- `POST /schedules/`
- `PUT /schedules/`
- `GET /schedules/`
- `GET /schedules/ping/{schedule_id}`

### Event history
- `GET /event-history/`
- `GET /event-history/{service_id}`
