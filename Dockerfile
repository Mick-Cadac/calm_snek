FROM python:latest AS build

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . .
RUN poetry build

FROM python:slim

WORKDIR /app

COPY --from=build /app/dist/*.whl .

RUN pip install *.whl

EXPOSE 6502
CMD ["gunicorn", "--bind", "0.0.0.0:6502", "main:app"]

