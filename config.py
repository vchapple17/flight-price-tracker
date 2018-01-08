# Val Chapple
#
# Nov 2018
# Updated Jan 8, 2018
# MIT License

import sys
import pymysql.cursors, pymysql.err
import plotly.offline as offline
import plotly.graph_objs as go

from datetime import datetime
import time

# Set up mysql database with files in sql folder
# import browser automation, such a selenium (requires python 2.7 only)
# MUST IMPLEMENT self._saveFlightPrices() on your own

class database:
    def __init__(self, u, p, h, d):

        # Connect to the database
        try:
            self._connection = pymysql.connect(host = h, user = u, password = p, db = d, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

        except pymysql.err.OperationalError as e:
            print(e[1])
            sys.exit()

    def __del__(self):
        try:
            self._conection.close()
            print("")
        except:
            print("")

    # Return mysql results of scheduled pricing jobs that are between
    # now and 6 months out.
    # Returns None if no results
    def _getActiveFutureJobs(self):
        try:
            with self._connection.cursor() as cursor:
                # Read All future and active jobs within 6 months
                sql = "SELECT j.job_id, j.day, j.dep, j.arr, j.class_type, j.status, c.code as dep, c2.code as arr FROM `job` j "
                sql += "INNER JOIN `city` c ON c.city_id = j.dep "
                sql += "INNER JOIN `city` c2 ON c2.city_id = j.arr "
                sql += "WHERE j.status=%s AND j.day >= CURDATE() AND j.day < DATE_ADD(now(), INTERVAL 6 MONTH);"
                cursor.execute(sql, "ACTIVE")
                result = cursor.fetchall()
                return result
        except:
            print("error getActiveFutureJobs")
            return None

    # Gets all active jobs
    def _getJobs(self):
        try:
            with self._connection.cursor() as cursor:
                # Read All active jobs
                sql = "SELECT j.job_id, j.day, j.dep, j.arr, j.class_type, j.status, c.code as dep, c2.code as arr FROM `job` j "
                sql += "INNER JOIN `city` c ON c.city_id = j.dep "
                sql += "INNER JOIN `city` c2 ON c2.city_id = j.arr;"
                cursor.execute(sql,)
                result = cursor.fetchall()
                return result
        except:
            print("error _getJobs")
            return None

    # Stub to use browser automation.
    def _saveFlightPrices(self, job):
        DEPARTURE = job["c.dep"]
        ARRIVAL = job["c2.arr"]
        try:
            DEPART_DATE = job["day"].strftime("%m/%d/%Y")
        except:
            print("Date conversion error")
            exit()
        FLIGHT_TYPE = job["class_type"]

        print("Job: " + DEPARTURE + " to " + ARRIVAL + " on " + DEPART_DATE + " class: " + FLIGHT_TYPE)

        # Get page with all flights listed for this one way trip
        # Iterate through each flight and save data with "self._saveFlightPrice()"
        # Save price , first flight number, Depart time, Arrival time,
        # Duration, and if nonstop (True or False)
        # Save

    # Use the three letter city code to look up the database city_id
    # Return None if error with MySql
    def _getCityIdFromCode(self, city_code):
        try:
            with self._connection.cursor() as cursor:
                # Read city id from code
                sql = "SELECT c.city_id, c.code FROM `city` c "
                sql += "WHERE c.code=%s;"
                cursor.execute(sql, city_code)
                result = cursor.fetchone()
                return result["city_id"]
        except:
            print("error _getCityIdFromCode:")
            print("sql: " + sql)
            print("city_code: " + city_code)
            return None

    # Get mysql flight id from flights that match parameters, else return None
    def _getFlightIdFromData(self, num, dep, arr, dur, nonstop, job_id):
        try:
            with self._connection.cursor() as cursor:
                # Read city id from code
                sql = "SELECT flight_id FROM `flight` "
                sql += "WHERE num=%s AND dep=%s AND arr=%s AND dur=%s AND nonstop=%s AND job=%s;"
                cursor.execute(sql, (num, dep, arr, dur, nonstop, job_id))
                result = cursor.fetchone()
                return result['flight_id']
        except:
            return  None

    # Find mysql flight_id or create a flight entry; return None for errors
    def _findOrCreate(self, num, dep, arr, dur, nonstop, job_id):
        depTime = time.strftime("%R", time.strptime(dep, "%I:%M %p"))
        arrTime = time.strftime("%R", time.strptime(arr, "%I:%M %p"))
        flight_id = self._getFlightIdFromData( num, depTime, arrTime, dur, nonstop, job_id)
        if flight_id != None:
            return flight_id
        else:
            # Add flight
            try:
                num = int(num)
            except:
                print("TypeError for integers: _saveFlight()")
                exit()

            try:
                with self._connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO flight (num, dep, arr, dur, nonstop, job) VALUES "
                    sql += "(%s, %s, %s, %s, %s, %s);"
                    cursor.execute(sql, (num, depTime, arrTime, dur, nonstop, job_id))
                self._connection.commit()
            except:
                print("ERROR: _saveFlight")
                return None
            return self._getFlightIdFromData( num, depTime, arrTime, dur, nonstop, job_id)

    # Save price of flight from parameters
    def _saveFlightPrice(self, dep, arr, day, type, num, depTime, arrTime, dur, price, nonstop, job_id):
        # Check if flight is in database and get id
        flight_id = self._findOrCreate( num, depTime, arrTime, dur, nonstop, job_id)

        # Save price
        try:
            price = int(price)
        except:
            print("TypeError for integers: _saveFlightPrice()")
            exit()

        try:
            with self._connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO price (price, flight) VALUES "
                sql += "(%s, %s);"
                cursor.execute(sql, (price, flight_id))
            self._connection.commit()
            print("SUCCESS: _saveFlightPrice")
        except:
            print("ERROR: _saveFlightPrice")

    # Query prices of flight from flight_id
    # Return array of created_on, price or None
    def _getPricesByFlightId(self, flight_id):
        try:
            with self._connection.cursor() as cursor:
                # Read
                sql = "SELECT created_on, price FROM `price` "
                sql += "WHERE flight=%s;"
                cursor.execute(sql, (flight_id))
                result = cursor.fetchall()
                return result
        except:
            return  None

    # Query all flights by job_id
    # Return array of flights (flight_id, num, dep, arr, dur, nonstop) or None
    def _getFlightsByJobId(self, job_id):
        try:
            with self._connection.cursor() as cursor:
                # Read city id from code
                sql = "SELECT flight_id, num, dep, arr, dur, nonstop FROM `flight` "
                sql += "WHERE job=%s;"
                cursor.execute(sql, (job_id))
                result = cursor.fetchall()
                return result
        except:
            return  None

    # Graph plot of flights in a single job on price vs. date graph
    # Saves a temp-plot.html file, and saves image as png
    def _graphJob(self, job):
        # print("GRAPHING JOB")
        offline.init_notebook_mode()

        # Job Info
        departCity = job["c.dep"]
        arriveCity = job["c2.arr"]
        day = job["day"]
        class_type = job["class_type"]

        # Graph File Name
        graph_name = "graph_"
        graph_name += departCity + "_"
        graph_name += arriveCity + "_"
        graph_name += str(day) + "_"
        graph_name += class_type

        flights = self._getFlightsByJobId( job["job_id"] )

        # Get flight prices
        data = []
        for f in flights:
            data_x = []
            data_y = []

            departTime = f["dep"] + datetime.strptime("2000-01-01", "%Y-%M-%d")
            data_name = (str(f["num"]) + " @ " + departTime.strftime("%I:%M %p")).lower()

            if f["nonstop"] == 1:
                data_name += (" ***")

            # Get Date and Prices Array for this flight
            date_price = self._getPricesByFlightId(f["flight_id"])
            for i in date_price:
                data_x.append(i["created_on"])
                data_y.append(int(i["price"]))

            if f["nonstop"] == 1:
                vis = True
            else:
                vis = "legendonly"

            data.append(
                go.Scatter(
                    x = data_x,
                    y = data_y,
                    mode = 'lines+markers',
                    name = data_name,
                    visible = vis
                )
            )
        # Graph Data
        layout = go.Layout(
            title=departCity + " to " + arriveCity + " on " + str(day),
            font=dict(size=16),
            width=800,
            height=640
        )

        offline.plot(
            { 'data': data, 'layout': layout},
            image='png'
        )
        return


    # Driver function to determine which job to graph
    def graphJobs(self):
        print("Select job to graph: ")
        # Get jobs
        result = self._getJobs()

        # Graph Selection MENU
        s = 0
        while s < 1 or s > n+1:
            n = len(result)
            for i in range(0, n):
                print(str(i+1) + " - " + result[i]["c.dep"] + " to " + result[i]["c2.arr"] + " on " + str(result[i]["day"]))
            print(str(n+1) + " - Back")

            prompt = ">> "
            s = raw_input(prompt)
            try:
                s = int(s)
            except:
                s = -1
        s -= 1  # Adjust selection s to match zero-indexing

        # Graph selected job
        self._graphJob(result[s])


    # Driver function to save prices for all jobs within the next 6months
    # Requires implementation of self._saveFlightPrices()
    def runPriceChecks(self):
        result = self._getActiveFutureJobs()
        for i in result:
            self._saveFlightPrices(i)
