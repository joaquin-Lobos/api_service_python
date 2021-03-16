#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.2

Descripcion:
Programa creado para administrar la base de datos de registro de personas
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.2"

import os
import sqlite3

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Persona(db.Model):
    __tablename__ = "persona"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String)
    age = db.Column(Integer)
    nationality = db.Column(String)
    
    def __repr__(self):
        return f"Persona:{self.name} con nacionalidad {self.nacionalidad}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(name, age, nationality):
    # Crear una nueva persona
    person = Persona(name=name, age=age, nationality=nationality)

    # Agregar la persona a la DB
    db.session.add(person)
    db.session.commit()


def report(limit=0, offset=0):
    # Obtener todas las personas
    query = db.session.query(Persona)
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    json_result_list = []

    # De los resultados obtenidos pasar a un diccionario
    # que luego será enviado como JSON
    # TIP --> la clase Persona podría tener una función
    # para pasar a JSON/diccionario
    for person in query:
        json_result = {'name': person.name, 'age': person.age, 'nationality': person.nationality}
        json_result_list.append(json_result)

    return json_result_list

def nationality_review():
    
    # Obtener los últimos 250 registros del paciente
    # ordenado por fecha, obteniedo los últimos 250 registros
    query = db.session.query(Persona)
    query = query.limit(250)
    query_results = query.all()

    if query_results is None or len(query_results) == 0:
        # No data register
        # Bug a proposito dejado para poner a prueba el traceback
        # ya que el sistema espera una tupla
        return []

    # De los resultados obtenidos tomamos el tiempo y las puslaciones pero
    # en el orden inverso, para tener del más viejo a la más nuevo registro
    id_persona = [x.id for x in query_results]
    age_persona = [x.age for x in query_results]

    return id_persona, age_persona
