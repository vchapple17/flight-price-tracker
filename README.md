# Flight Price Tracker

Uses Plot.ly to graph the price of nonstop flights for a given one-way flight request.  Provides stubs to implement your own price gathering code (for me to avoid potential legal issues with specific airlines).  In my private copy of this repo, I use Selenium to gather price information from my preferred airline.  Selenium for Mac runs with Python 2.7.

## Getting Started

_Setup Mysql_

Use the provided schema and data in the `sql` folder to setup a database with example flight data.

_Graph Example Data_

Use Python 2.7 to run `python main.py`.  Here you will be presented with a menu to: 
* gather prices _(you'll have to implement code first)_
* graph prices _(there is mock data in the database)_

## Add your own flight job

For now, you'll have to manually add a job to the database.

**Example:**
```
INSERT INTO job (day, dep, arr, class_type) VALUES
('2018-02-02', 54, 45, 'C'),
('2018-02-05', 45, 54, 'C');
```
_Note_: You will need to know the city_id of the cities you are departing from and arriving at.  For this data, use the three letter airport code, such as MCI for Kansas City Internation airport and a MySQL query, such as `SELECT * FROM city WHERE code = 'MCI';`

## Implement Your Own Code

In `config.py`, you will need to write your own code to gather prices from a website for active jobs within 6 moths. I chose to use Selenium and hardcode my favorite URL.  I manually had to inspect the website to know which elements to reference in order to gather the flight information.

## Graph

When graphing prices, you must select a job you wish to run.  The graph will be in HTML and automatically generate a png file.  The graph has multiple traces (one per flight) with a y-axis of price and an x-axis of date.

## Author

* **Valerie Chapple** - [vchapple17](https://github.com/vchapple17)

## License

This project is licensed under the MIT License.
