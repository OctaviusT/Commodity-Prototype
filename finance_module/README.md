# Finance Module

This module contains the `finance_prototype.db` SQLite database and Python scripts
used to import and query financial data for the Commodity Prototype project.

## Purpose
The finance module manages company financials and supports correlation analysis
between financial health and commodity trading data. It serves as a data source
that complements the commodities module.

## Structure
- `finance_prototype.db` → SQLite database with two main tables:
  - **companies**: stores company information
  - **financials**: stores financial statement data
- `import_fdb.py` → Example Python script showing how to query and pull data.

## Relation to Commodity Prototype
The financials stored here can be merged with the commodity trading data from
the commodities module. This allows testing strategies that link company 
financial performance with commodity market movements.

