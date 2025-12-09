# Arkanoid 3D

Arkanoid 3D adalah game arkanoid sederhana dengan tampilan 3D menggunakan Python.  
Game ini berjalan menggunakan tiga library utama:

- `pygame`
- `PyOpenGL`
- `numpy`

Semua dependensi tersebut akan di-install otomatis melalui `run_game.bat`.

---

## Cara Install & Menjalankan

1. **Install Python 3.11.0**

   - [64-bit](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe)  
   - [32-bit](https://www.python.org/ftp/python/3.11.0/python-3.11.0.exe)

2. Setelah Python selesai dipasang, cukup jalankan dengan double-click:

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
├── .idea/
├── .venv/
├── pycache/
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
