# Arkanoid 3D

Arkanoid 3D adalah game arkanoid sederhana dengan tampilan 3D menggunakan Python.  
Game ini berjalan menggunakan tiga library utama:

- `pygame`
- `PyOpenGL`
- `numpy`

Semua dependensi tersebut akan di-install otomatis melalui `run_game.bat`.

---

## Cara Install & Menjalankan

### 1. **Install Python 3.11.0**

Unduh installer:

- [64-bit](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe)  
- [32-bit](https://www.python.org/ftp/python/3.11.0/python-3.11.0.exe)

Saat membuka installer:

1. **Jangan** langsung klik *Install Now*  
2. Pilih **Customize installation**  
3. **Jangan centang** opsi **“Add python.exe to PATH”**  
4. Lanjutkan Next → Install

Setelah Python selesai dipasang, lanjutkan ke langkah berikutnya.

---

### 2. **Jalankan Game**

Cukup double-click:

```bash
run_game.bat
```

Script tersebut akan:
- memastikan Python 3.11 tersedia  
- membuat virtual environment `.venv`  
- meng-install pygame, PyOpenGL, dan numpy  
- menjalankan game  
- menutup environment setelah selesai  

---

## Struktur Project

```
arkanoid-3d/
├── .gitignore
├── background.jpeg
├── background.jpg
├── Ball.py
├── Brick.py
├── Color.py
├── draw_cube.py
├── Game.py
├── main.py
├── MouseEvent.py
├── Paddle.py
├── README.md
├── run_game.bat
└── Table.py
```


---
