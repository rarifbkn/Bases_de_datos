query = "select rut from cliente where rut=%s"
data, = select_query(query,[rut])[0]
print(data)