# Query Cannon

```
qcan --help
qcan fire 8.8.8.8 loop www.google.com 20
```

## Commands

```
qcan fire 8.8.8.8 loop www.google.com 20
qcan fire 8.8.8.8 para www.google.com 5 2
qcan fire 10.15.190.71 urlpara urls.txt 5 2
```

## Mac / Linux

### Setup Virtual Environment and Activate

```
python3 -m venv .env
source .env/bin/activate
pip install  -e .
qcan fire 8.8.8.8 para www.google.com 5 2
```

## Windows

Note that ray is not available at this time so para execution is mac/linux only at this time.  

### Setup Virtual Environment and Activate

```
python -m venv .env
.\.env\Scripts\Activate.ps1
```
