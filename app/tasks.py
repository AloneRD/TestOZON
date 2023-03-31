from app.celery import app


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    print("Вижуууу")
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test_task.s(), name="add every 10")


@app.task
def test_task():
    print("Таска сельдерея работает")
