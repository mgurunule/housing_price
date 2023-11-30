import pandas as pd
import os
import sqlite3
from housing_price.constants.db_constants import (
    DB_DIR,
    DB_NAME,
    PREDICTED_DATA_TABLE_NAME,
    PREDICTION_CREATE_QUERY_PATH,
    TRANSFORMED_DATA_TABLE_NAME,
    TRANSFORMED_CREATE_QUERY_PATH,
)


class DataBaseOperation:
    """
        Description: : This class shall be used for handling all the SQL operations
        for example :
                1) DB connection : Establishing the connection to DataBase
                2) DB creation   : Creating the DataBase
                3) DB insertion  : Inserting the value in DataBase
                4) DB selection  : Fetching the data from DataBase
    """

    def __init__(self, path, logger):
        self.logger = logger
        self.path = path

    def database_connection(self,
                            database_name: str
                            ):
        """
             Description : This method opens the connection to the passed
                          database. If the database is not available
                          then creates and new DB.
        Parameters
        ----------
        database_name: str
                       name of the database

        Returns
        -------
        on success : sqlite conncection object
        on Failure  : Raise ConnectionError
        """
        try:
            db_complete_path = os.path.join(self.path, DB_DIR, database_name)

            conn = sqlite3.connect(db_complete_path)

            self.logger.info(f"Opened {database_name} database successfully")

        except ConnectionError as ce:
            self.logger.error(f"DB CONNECTION FAILED.Got "
                              f"{ce.__class__.__name__} exception: {ce}")
            raise ce
        except Exception as e:
            self.logger.error(f"DB CONNECTION FAILED.Got "
                              f"{e.__class__.__name__} exception: {e}")
            raise e

        return conn

    def create_db_table(self, database_name: str, table_name: str) -> None:
        """
           Description : create table in the given database.

        Parameters
        ----------
        database_name: str
                    Name of the database
        table_name: name of the new table

        Returns
        -------
        None
        """

        try:
            conn = self.database_connection(database_name)

            query_path = ""
            cursor = conn.cursor()
            if table_name == PREDICTED_DATA_TABLE_NAME:
                query_path = os.path.join(self.path,
                                          PREDICTION_CREATE_QUERY_PATH)
            elif table_name == TRANSFORMED_DATA_TABLE_NAME:
                query_path = os.path.join(self.path,
                                          TRANSFORMED_CREATE_QUERY_PATH)
            with open(query_path, 'r') as sqlite_file:
                sql_script = sqlite_file.read()

            cursor.executescript(sql_script)
            self.logger.info(f"{table_name} table created successfully")

        except sqlite3.Error as error:
            self.logger.error(f" Error while creating table {error}")
        finally:
            conn.close()
            self.logger.info(" Closed database successfully")

    def insert_into_table(self,
                          database_name: str,
                          data: pd.DataFrame,
                          table_name: str
                          ):
        """
            Description : Insert the given data to table af given database.

        Parameters
        ----------
        database_name: str
                Name of the database.
        data: pd.DataFrame
               DataFrame that needs to be inserted.
        table_name: str
               Name of the table in which data need to be inserted
        """
        try:
            conn = self.database_connection(database_name)

            data.to_sql(table_name, conn, if_exists='append', index=False)
            conn.commit()
            self.logger.info(f" Records inserted Successfully in {table_name}")

        except sqlite3.Error as error:
            self.logger.error(f" ERROR in insertion : {error}")
            conn.rollback()
            self.logger.error(f" ROLLBACK CHANGES from {table_name} database")
            raise
        except Exception as e:
            self.logger.error(f" ERROR in inserting the data to "
                              f"{table_name} database: {e}")
            conn.rollback()
            self.logger.error(f" ROLLBACK CHANGES from {table_name} database")
            raise
        finally:
            conn.close()
            self.logger.info(" Closed database successfully")

    def select_data_from_table(self, database_name: str, table_name: str):
        """
           Description : fetch the record from the given table

        Parameters
        ----------
        database_name: str
                       Name of the database name
        table_name: str
                    Table from which data need to be fetched
        Returns
        -------
        pd.DataFrame
            return fetched data in the form of dataframe
        """

        try:
            conn = self.database_connection(database_name)

            sql_select = f"SELECT * FROM {table_name}"
            query = conn.execute(sql_select)
            cols = [column[0] for column in query.description]
            results = pd.DataFrame.from_records(
                data=query.fetchall(), columns=cols)
            self.logger.info(f" Records fetched successfully"
                             f" from {table_name}")
            return results

        except sqlite3.Error as error:
            self.logger.error(f" ERROR while fetching : {error}")
        except Exception as e:
            self.logger.error(f" Error in fetching the details from "
                              f"{table_name} table:  {e}")
            raise
        finally:
            conn.close()
            self.logger.info(" Closed database successfully")
