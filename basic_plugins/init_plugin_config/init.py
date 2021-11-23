from utils.manager import plugins2settings_manager


def init():
    if plugins2settings_manager.get("update_pic"):
        plugins2settings_manager["update_picture"] = plugins2settings_manager["update_pic"]
        plugins2settings_manager.delete("update_pic")
    if plugins2settings_manager.get("white2black_img"):
        plugins2settings_manager["white2black_image"] = plugins2settings_manager["white2black_img"]
        plugins2settings_manager.delete("white2black_img")
    if plugins2settings_manager.get("send_img"):
        plugins2settings_manager["send_image"] = plugins2settings_manager["send_img"]
        plugins2settings_manager.delete("send_img")

