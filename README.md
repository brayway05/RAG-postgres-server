## Docker Commands for Postgres

_**get this to run on something else and serve it_

Build Image:
`docker build -t postgres-image .`

Create and start container:
`docker run --name postgres-container -p 5432:5432 -v postgres_data:/var/lib/postgresql/data -d postgres-image`

Start container:
`docker start postgres-container`

Check running containers:
`docker ps`

Connect to Postgres shell:
`docker exec -it postgres-container psql -U myuser -d mydb`

## Python env (mac arm64)

`conda create -n postgres python=3.10`

`conda activate postgres`

`conda install pip`

`pip install -r requirements.txt`

## Python Scripts

Insert new document into VectorDB:
`python embed_insert.py --file_path /path/to/your/document.txt --chunk_size 1000 --doc_title "My Document Title" --doc_owner "Document Owner"`

Query the VectorDB:
`python query.py`

MORE HERE