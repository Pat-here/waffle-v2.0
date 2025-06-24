# Gofry Dashboard - Aplikacja dla Budki z Goframi

Kompleksowa aplikacja webowa Flask do zarządzania budką z goframi.

## Funkcjonalności

### 🔐 System logowania
- Bezpieczne logowanie (admin/admin123)
- Sesje użytkowników
- Wylogowanie

### 📊 Dashboard
- Przegląd kluczowych metryk
- Wykresy sprzedaży
- Statystyki w czasie rzeczywistym
- Stan magazynowy

### 🛍️ Zarządzanie produktami
- Dodawanie składników
- Kategorie produktów
- Śledzenie kosztów i stanów
- Alerty niskiego stanu

### 🧁 Kompozycje gofrów
- Tworzenie gotowych produktów
- Kalkulacja marży
- Ceny sprzedaży
- Status produktów

### 📝 Notatki
- Zapisywanie uwag
- Organizacja notatek
- Znaczniki czasowe

### ⏰ Czas pracy
- Śledzenie godzin pracowników
- Historia czasu pracy
- Opisy zmian

### 📈 Raporty
- Dzienne podsumowania sprzedaży
- Miesięczne zestawienia
- Analiza zyskowności
- Trendy sprzedaży

### 🛒 Lista zakupów
- Automatyczne generowanie list
- Priorytetyzacja zakupów
- Status zamówień

### 🧮 Kalkulator lokalny
- Kalkulacja kosztów kompozycji
- Analiza marży
- Optymalizacja cen

## Wymagania techniczne

- Python 3.11+
- Flask 2.3+
- SQLAlchemy
- Bootstrap 5
- Chart.js

## Instalacja lokalna

1. Sklonuj projekt:
```bash
git clone <repository-url>
cd gofry_dashboard
```

2. Utwórz wirtualne środowisko:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Uruchom aplikację:
```bash
python app.py
```

5. Otwórz w przeglądarce: `http://localhost:5000`

## Wdrożenie na Render

### Przygotowanie
1. Utwórz konto na [Render.com](https://render.com)
2. Połącz z kontem GitHub
3. Umieść kod w repozytorium GitHub

### Konfiguracja
1. W Render Dashboard kliknij "New" → "Web Service"
2. Połącz repozytorium GitHub
3. Użyj następujących ustawień:

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python app.py
```

**Environment Variables:**
- `FLASK_ENV`: `production`
- `SECRET_KEY`: (generuj automatycznie)

### Automatyczne wdrożenie
Render automatycznie wykryje:
- `requirements.txt` - zależności Python
- `render.yaml` - konfigurację serwisu
- `Procfile` - komendy uruchomienia

## Struktura projektu

```
gofry_dashboard/
├── app.py                 # Główna aplikacja Flask
├── requirements.txt       # Zależności Python
├── render.yaml           # Konfiguracja Render
├── Procfile              # Komendy wdrożenia
├── runtime.txt           # Wersja Python
├── .gitignore           # Pliki do ignorowania
├── app/
│   ├── templates/        # Szablony HTML
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── products.html
│   │   ├── compositions.html
│   │   ├── notes.html
│   │   ├── worktime.html
│   │   ├── reports.html
│   │   ├── shopping.html
│   │   ├── calculator.html
│   │   └── add_*.html
│   └── static/           # Pliki statyczne
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
└── README.md
```

## Baza danych

Aplikacja używa SQLite z następującymi tabelami:
- `users` - użytkownicy systemu
- `products` - składniki i produkty
- `compositions` - gotowe kompozycje gofrów
- `composition_ingredients` - składniki kompozycji
- `notes` - notatki
- `work_time` - czas pracy pracowników
- `reports` - raporty dzienne
- `shopping_items` - lista zakupów

## Bezpieczeństwo

- Hashowanie haseł (Werkzeug)
- Ochrona CSRF (Flask-WTF)
- Walidacja formularzy
- Sesje zabezpieczone
- Ochrona przed SQL injection

## Dane testowe

Po pierwszym uruchomieniu system automatycznie utworzy:
- Konto administratora: `admin` / `admin123`
- Przykładowe produkty
- Przykładowe kompozycje
- Przykładowe notatki

## Wsparcie

W przypadku problemów:
1. Sprawdź logi aplikacji
2. Zweryfikuj konfigurację środowiska
3. Upewnij się, że wszystkie zależności są zainstalowane

## Licencja

Projekt stworzony dla potrzeb zarządzania budką z goframi.
