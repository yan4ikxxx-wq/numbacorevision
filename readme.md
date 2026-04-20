<img width="650" height="649" alt="CHECK" src="https://github.com/user-attachments/assets/78d47872-e231-4441-bd27-3675428ad95a" />
Система управления курсором Windows с помощью жестов рук,
оптимизированная для работы в условиях сложного освещения. 
Использует компьютерное зрение и высокопроизводительные вычисления на Numba.

---

"Enjoying this project? Buy me a coffee 🚀"
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/donate/?hosted_button_id=S4AH7LV44BT9N)

[English version below](#english)

---

## Особенности (RU) 🇷🇺
- **Плавность движения:** Физика курсора просчитывается через **Numba (@njit)**, что исключает задержки (input lag).
- **Адаптивное зрение:** Использование фильтра **CLAHE** и алгоритма **OTSU** позволяет системе видеть руку даже при плохом освещении.
- **Динамическая калибровка:** Система автоматически подстраивает чувствительность при смене режимов.
- **Интерфейс "Картинка в картинке" (PIP):** Вы всегда видите, как нейросеть обрабатывает ваше изображение в реальном времени.

### Требования
- ОС: Windows 8.1/10/11
- Веб-камера (рекомендуется 30+ FPS)
- Python 3.9+

### Управление
1. **MOUSE:** Управление курсором (запястье — ведущая точка). Клик — сведение большого и указательного пальцев.
2. **SCROLL:** Лайк (большой палец вверх) — скролл вверх, жест "V" — скролл вниз.
3. **TURBO:** Режим повышенной скорости курсора.
* **Смена режима:** Удерживайте мизинец поднятым в течение 1 секунды.

### Быстрые клавиши
- `I` — Инверсия бинарной маски (если рука черная на белом).
- `ESC` — Выход.

Важное примечание: Антивирус и безопасность
 Поскольку программа NUMBA_3 скомпилирована в один исполняемый файл (.exe)
 и не имеет дорогостоящей цифровой подписи издателя,
 некоторые антивирусы (включая Windows Defender) могут ошибочно принять
 её за угрозу (False Positive).

Как запустить:

Если при запуске появилось окно «Система Windows защитила ваш компьютер» 
— нажмите «Подробнее», а затем «Выполнить в любом случае».

Если файл блокируется антивирусом — добавьте папку с программой в список исключений.

Проект имеет открытый исходный код, поэтому вы всегда можете 
проверить его на отсутствие вредоносных вставок здесь, в репозитории.

---

<a name="english"></a>
## Features (EN) 🇺🇸
- **Ultra-Smooth Motion:** Cursor physics calculated via **Numba (@njit)** for zero-latency performance.
- **Adaptive Vision:** **CLAHE** filtering combined with **OTSU** thresholding ensures stable hand tracking in various lighting conditions.
- **Dynamic Calibration:** Real-time auto-sensitivity adjustment during gesture transitions.
- **PIP Interface:** Live "Neural View" preview window built into the main feed.

### Requirements
- OS: Windows 8.1/10/11
- Webcam (30+ FPS recommended)
- Python 3.9+

### Controls
1. **MOUSE:** Cursor control (Wrist-based). Pinch thumb and index finger to click.
2. **SCROLL:** Thumb up to scroll up, "V" gesture to scroll down.
3. **TURBO:** High-speed cursor movement.
* **Mode Switch:** Hold your pinky finger up for 1 second.

### Hotkeys
- `I` — Invert binary mask (useful if the hand is not detected properly).
- `ESC` — Exit application.

---

## Installation / Установка ⚙️



Install dependencies / Установите зависимости:



pip install -r requirements.txt

Ensure hand_landmarker.task is in the project folder. / Убедитесь, что файл модели hand_landmarker.task находится в папке проекта.

Run / Запуск:

python main.py    название файла основного/main file name


Note on Antivirus: > Since the executable is not digitally signed,
 Windows Defender or other antivirus software may flag it as a "False Positive".
 Solution: Add the program folder to your antivirus exclusions or click 
 "Run anyway" in the Windows SmartScreen popup.


"Enjoying this project? Buy me a coffee 🚀"
 [![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/donate/?hosted_button_id=S4AH7LV44BT9N)
