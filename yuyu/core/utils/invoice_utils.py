def state_to_text(state):
    if state == 1:
        return 'In Progress'
    if state == 2:
        return 'Unpaid'
    if state == 100:
        return 'Finished'
