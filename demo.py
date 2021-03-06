from flypper.wsgi.web_ui import FlypperWebUI
from sqlalchemy import (
    create_engine,
    MetaData,
)
from werkzeug.serving import run_simple

from flypper_sqlalchemy.storage.sqla import SqlAlchemyStorage

# Be sure to create a demo.sqlite3 DB first by running:
#
#   $ sqlite3 file.db "VACUUM;"
engine = create_engine('sqlite:///demo.sqlite3')

metadata = MetaData()
flypper_metadata = SqlAlchemyStorage.build_metadata_table(metadata)
flypper_flags = SqlAlchemyStorage.build_flags_table(metadata)
metadata.create_all(engine)

storage = SqlAlchemyStorage(engine=engine)

storage.upsert({
    "name": "fr_api.prod.on_demand_feature",
    "enabled": True,
    "enabled_for_actors": {
        "actor_key": "user_id",
        "actor_ids": ["8", "42", "200000"],
    },
    "enabled_for_percentage_of_actors": None,
    "deleted": False,
})
storage.upsert({
    "name": "fr_api.prod.rolling_out_feature",
    "enabled": True,
    "enabled_for_actors": None,
    "enabled_for_percentage_of_actors": {
        "actor_key": "user_id",
        "percentage": 10.00,
    },
    "deleted": False,
})
storage.upsert({
    "name": "fr_api.prod.fully_rolled_out_feature",
    "enabled": True,
    "enabled_for_actors": None,
    "enabled_for_percentage_of_actors": None,
    "deleted": False,
})
storage.upsert({
    "name": "fr_api.prod.failover_for_payments",
    "enabled": False,
    "enabled_for_actors": None,
    "enabled_for_percentage_of_actors": None,
    "deleted": False,
})

app = FlypperWebUI(storage=storage)
run_simple("127.0.0.1", 5000, app, use_debugger=True, use_reloader=True)
