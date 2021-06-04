from tools.log import log, warn
import sqlite3
import atexit
import os


dbfile = "answerable.db"
db = None


def create_db():
    global db
    with db:
        log("Building database")
        db.executescript(
            """
        
        CREATE TABLE QUESTION (
            ID              INT         PRIMARY KEY NOT NULL,
            TITLE           CHAR(100)   NOT NULL,
            BODY            TEXT        NOT NULL,
            CREATION_DATE   TIMESTAMP   NOT NULL,
            SCORE           INT         NOT NULL,
            ACCEPTED_ANSWER INT,
            LAST_UPDATED_DB TIMESTAMP
        );
        
        CREATE TRIGGER SET_LAST_UPDATED_QUESTION_INSERT
            AFTER INSERT ON QUESTION
            FOR EACH ROW 
        BEGIN
            UPDATE QUESTION
                SET LAST_UPDATED_DB = strftime('%s', 'now')
                WHERE ID = NEW.ID;
        END;
        
        CREATE TRIGGER SET_LAST_UPDATED_QUESTION_UPDATE
            AFTER UPDATE ON QUESTION
            FOR EACH ROW 
        BEGIN
            UPDATE QUESTION
                SET LAST_UPDATED_DB = strftime('%s', 'now')
                WHERE ID = NEW.ID;
        END;
        
        CREATE TABLE DISCARDED_QUESTIONS (ID INT);
        
        CREATE TABLE QUESTION_TAG (
            QUESTION_ID INT         NOT NULL,
            TAG         CHAR(25)    NOT NULL
        );
        CREATE INDEX QUESTION_TAG_QUESTION_ID_IDX ON QUESTION_TAG(QUESTION_ID);

        CREATE TABLE USER_ANSWERS (
            ID          INT     PRIMARY_KEY NOT NULL,
            BODY        TEXT    NOT NULL,
            QUESTION_ID INT     NOT NULL,
            SCORE       INT     NOT NULL,
            IS_ACCEPTED BOOLEAN NOT NULL,
            USER_ID     INT     NOT NULL
        );
        CREATE INDEX ANSWER_QUESTION_ID_IDX ON USER_ANSWERS(QUESTION_ID);
        
        CREATE TABLE QUESTION_ANSWER (
            QUESTION_ID INT NOT NULL,
            ANSWER_ID   INT NOT NULL    
        );
        CREATE INDEX QUESTION_ANSWER_QUESTION_ID ON QUESTION_ANSWER(QUESTION_ID);
        
        
        CREATE TRIGGER ON_DELETE_QUESTIONS
            BEFORE DELETE ON QUESTION
            FOR EACH ROW 
        BEGIN
            INSERT INTO DISCARDED_QUESTIONS VALUES (OLD.ID);
            DELETE FROM QUESTION_TAG WHERE QUESTION_ID = OLD.ID;
            DELETE FROM QUESTION_ANSWER WHERE QUESTION_ID = OLD.ID;
        END;
        
        """
        )


def save_questions(questions):
    if(len(questions) == 0):
        return
    global db
    insert_question = """
        INSERT INTO QUESTION 
            (ID, TITLE, BODY, CREATION_DATE, SCORE, ACCEPTED_ANSWER)
        VALUES 
            (:question_id, :title, :body, :creation_date, :score, :accepted_answer_id)
    """
    insert_question_tag = """
        INSERT INTO QUESTION_TAG VALUES (?, ?)
    """
    insert_question_answer = """
        INSERT INTO QUESTION_ANSWER VALUES (?, ?)
    """
    values_q_t = [(q["question_id"], t) for q in questions for t in q["tags"]]
    values_q_a = [
        (q["question_id"], a["owner"]["user_id"])
        for q in questions
        for a in q["answers"]
    ]
    with db:
        db.executemany(insert_question, questions)
        db.executemany(insert_question_tag, values_q_t)
        db.executemany(insert_question_answer, values_q_a)
    log("New questions saved")


def update_questions(questions):
    if len(questions) == 0:
        return
    global db
    update_sentences = [
        """
            UPDATE QUESTION 
                SET
                    TITLE = :title,
                    BODY = :body,
                    SCORE = :score,
                    ACCEPTED_ANSWER = :accepted_answer_id
                WHERE ID = :question_id;
        """,
        "DELETE FROM QUESTION_TAG WHERE QUESTION_ID = :question_id;",
        "DELETE FROM QUESTION_ANSWER WHERE QUESTION_ID = :question_id;",
    ]
    insert_question_tag = "INSERT INTO QUESTION_TAG VALUES (?, ?)"
    insert_question_answer = "INSERT INTO QUESTION_ANSWER VALUES (?, ?)"
    values_q_t = [(q["question_id"], t) for q in questions for t in q["tags"]]
    values_q_a = [
        (q["question_id"], a["owner"]["user_id"])
        for q in questions
        for a in q["answers"]
    ]
    with db:
        for s in update_sentences:
            db.executemany(s, questions)
        db.executemany(insert_question_tag, values_q_t)
        db.executemany(insert_question_answer, values_q_a)
        log("Old questions updated")


def filter_qids_for_update(qids, oldest, cache_time):
    global db
    with db:
        return {
            x
            for (x,) in db.execute(
                """
                SELECT ID FROM QUESTION
                    WHERE (strftime('%s', 'now') - CREATION_DATE) < ?
                      AND (strftime('%s', 'now') - LAST_UPDATED_DB) > ?
            """,
                (oldest, cache_time)
            )
            if x in qids
        }


def filter_qids_for_insert(qids):
    global db
    with db:
        return qids - {
            x
            for (x,) in db.execute(
                "SELECT ID FROM QUESTION UNION SELECT ID FROM DISCARDED_QUESTIONS"
            )
        }


def delete_questions_older_than(quantity):
    global db
    with db:
        return [
            row[0]
            for row in db.execute(
                """
                DELETE FROM QUESTION 
                WHERE (strftime('%s', 'now') - CREATION_DATE) > ?
                  AND ID NOT IN (SELECT QUESTION_ID FROM USER_ANSWERS)
            """,
                quantity,
            )
        ]


def setup():
    global db
    if os.path.isfile(dbfile):
        log("Opening database")
        db = sqlite3.connect(dbfile)
    else:
        log("Database not found. Create one")
        db = sqlite3.connect(dbfile)
        create_db()


def close():
    global db
    db.close()
