*** settings ***
resource  resrc
#suite setup  init
test setup  init

*** test cases ***

TC 1
    [tags]  B____B
    log to console  A_____A
    log    A______________A   console=True


TC 3
    [template]  log to console
    K________K
    T_____T
