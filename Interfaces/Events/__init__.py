from Core.event import trigger_invoke, trigger_failed, trigger_return, listen_event as on

def on_card_creating():
    return on(event_name='card.creating')

def on_card_created():
    return on(event_name='card.created')

def on_card_building():
    return on(event_name='card.building')

def on_card_builded():
    return on(event_name='card.builded')