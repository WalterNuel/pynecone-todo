import pynecone as pc

class PctodoConfig(pc.Config):
    pass

config = PctodoConfig(
    app_name="pc_todo",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)