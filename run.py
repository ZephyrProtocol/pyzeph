PminRc = 0.5 #ZEPH
total_reserves = 0 # 0 ZEPH in reserve
number_stable_coins = 0 # 0 ZUSD in circulation
number_reserve_coins = 0 # 0 ZRSV in circulation
spot = 0
ma = 0
fee = 0.02

def print_state():
    print('\n======= Network State =======')
    print('Price:          spot$', spot)
    print('                  ma$', ma)
    print('-----------------------------')
    print('Reserve:             ', total_reserves, 'ZEPH')
    print('                    $', total_reserves * spot)
    print('                  ma$', total_reserves * ma)
    print('-----------------------------')
    print('Number Stable Coins: ', number_stable_coins)
    print('Number Reserve Coins:', number_reserve_coins)
    print('Reserve Ratios(s/ma):', reserve_ratio())
    print('==============================\n')

def conversion_rate(tt, spot, ma):
    if tt == 'mint_stable':
        return min(spot,ma)
    elif tt == 'redeem_stable':
        return max(spot,ma)
    elif tt == 'mint_reserve':
        return max(spot,ma)
    elif tt == 'redeem_reserve':
        return min(spot,ma)
    else:
        raise Exception('Invalid trade type')


def stable_price_target():
    # cr
    return 1

# def reserve_ratio():
#     global total_reserves
#     global number_stable_coins
#     if number_stable_coins != 0:
#         return total_reserves * spot / number_stable_coins

def reserve_ratio():
    global total_reserves
    global number_stable_coins
    if number_stable_coins != 0:
        rr_spot = total_reserves * spot / number_stable_coins
        rr_ma = total_reserves * ma / number_stable_coins
    else:
        rr_spot = rr_ma = float('inf')
    return rr_spot, rr_ma

def reserve_ratio_check(total_reserves, number_stable_coins):
    if number_stable_coins != 0:
        rr_spot = total_reserves * spot / number_stable_coins
        rr_ma = total_reserves * ma / number_stable_coins
    else:
        rr_spot = rr_ma = float('inf')
    return rr_spot, rr_ma

def equity(tt):
    global total_reserves
    global number_stable_coins
    global spot
    global ma
    return total_reserves - number_stable_coins / conversion_rate(tt, spot, ma)

def price_target_rc(tt):
    global number_reserve_coins
    try:
        return equity(tt) / number_reserve_coins
    except ZeroDivisionError:
        return None

def buying_price_rc(tt):
    global PminRc
    ptrc = price_target_rc(tt)
    if ptrc is None: #check if ptrc is undefined
        return PminRc
    else:
        return max(ptrc, PminRc)
    
def calculate_redeem_res_fee(rr):
    fee = -33.33 * rr + 133.33
    fee = max(0, fee)    # fee should not be less than 0
    fee = min(100, fee)  # fee should not exceed 100
    return fee
    
### actions
# def mint_stable_coins(zeph_amount_spent):
#     tt = 'mint_stable'
#     cr = conversion_rate(tt, spot, ma)
#     stable_coins_minted = zeph_amount_spent * cr * (1-fee)

#     global total_reserves
#     global number_stable_coins
#     total_reserves += zeph_amount_spent
#     number_stable_coins += stable_coins_minted
#     return stable_coins_minted

# def redeem_stable_coins(zusd_amount_spent):
#     tt = 'redeem_stable'
#     cr = conversion_rate(tt, spot, ma)
#     rr = reserve_ratio()
#     print(f'Called -> redeem_stable_coins({zusd_amount_spent})')
#     print(f'        cr: {cr}')
#     print(f'        rr: {rr}')
    
#     zeph_received = (zusd_amount_spent / cr) * (1-fee)
#     print(f'        zeph_ideal_amount: {zeph_received}')
#     if rr < 1:
#         print('        !!!! rr < 1 - going to receive zeph proprotional to reserve_ratio')
#         zeph_received = zeph_received * rr #worst case scenario

#     global total_reserves
#     global number_stable_coins
#     total_reserves -= zeph_received
#     number_stable_coins -= zusd_amount_spent
#     return zeph_received

# def mint_reserve_coins(zeph_amount_spent):
#     tt = 'mint_reserve'
#     reserve_coins_minted = zeph_amount_spent / buying_price_rc(tt)

#     global total_reserves
#     global number_reserve_coins
#     total_reserves += zeph_amount_spent
#     number_reserve_coins += reserve_coins_minted
#     return reserve_coins_minted

# def redeem_reserve_coins(zrs_amount_spent):
#     tt = 'redeem_reserve'
#     zeph_received = zrs_amount_spent * buying_price_rc(tt)

#     global total_reserves
#     global number_reserve_coins
#     total_reserves -= zeph_received
#     number_reserve_coins -= zrs_amount_spent
#     return zeph_received
def mint_stable_coins(zeph_amount_spent):
    global total_reserves
    global number_stable_coins

    new_total_reserves = total_reserves + zeph_amount_spent
    new_number_stable_coins = number_stable_coins + (zeph_amount_spent * conversion_rate('mint_stable', spot, ma) * (1-fee))

    r, r24 = reserve_ratio_check(new_total_reserves, new_number_stable_coins)
    print(f'Called -> mint_stable_coins({zeph_amount_spent})')
    print(f'        r: {r}')
    print(f'        r24: {r24}')
    if r < 4 or r24 < 4:
        print('Action denied: Reserve ratios must be above 4.0 to mint stable coins.')
        return


    total_reserves = new_total_reserves
    number_stable_coins = new_number_stable_coins
    return number_stable_coins

def redeem_stable_coins(zusd_amount_spent):
    global total_reserves
    global number_stable_coins

    tt = 'redeem_stable'
    cr = conversion_rate(tt, spot, ma)
    rr_spot, rr_ma = reserve_ratio()
    print(f'Called -> redeem_stable_coins({zusd_amount_spent})')
    print(f'        cr: {cr}')
    print(f'        rr_spot: {rr_spot}')
    print(f'        rr_ma: {rr_ma}')
    
    zeph_received = (zusd_amount_spent / cr) * (1-fee)
    print(f'        zeph_ideal_amount: {zeph_received}')
    if rr_spot < 1:
        print('        !!!! rr_spot < 1 - going to receive zeph proportional to reserve_ratio')
        zeph_received = zeph_received * rr_spot #worst case scenario


    total_reserves -= zeph_received
    number_stable_coins -= zusd_amount_spent
    return zeph_received

def mint_reserve_coins(zeph_amount_spent):
    global total_reserves
    global number_reserve_coins

    new_total_reserves = total_reserves + zeph_amount_spent
    new_number_reserve_coins = number_reserve_coins + (zeph_amount_spent / buying_price_rc('mint_reserve'))

    r, r24 = reserve_ratio_check(new_total_reserves, new_number_reserve_coins)
    print(f'Called -> mint_reserve_coins({zeph_amount_spent})')
    print(f'        r: {r}')
    print(f'        r24: {r24}')
    if r > 8 or r24 > 8:
        print('Action denied: Reserve ratios must be below 8.0 to mint reserve coins.')
        return


    total_reserves = new_total_reserves
    number_reserve_coins = new_number_reserve_coins
    return number_reserve_coins

def redeem_reserve_coins(zrs_amount_spent):
    tt = 'redeem_reserve'
    global total_reserves
    global number_reserve_coins
    global number_stable_coins
    zeph_received = zrs_amount_spent * buying_price_rc(tt)

    new_total_reserves = total_reserves - zeph_received
    new_number_reserve_coins = number_reserve_coins - zrs_amount_spent

    r, r24 = reserve_ratio_check(new_total_reserves, number_stable_coins)
    print(f'Called -> redeem_reserve_coins({zrs_amount_spent})')
    print(f'        r: {r}')
    print(f'        r24: {r24}')
    if (r < 4 or r24 < 4) and number_stable_coins != 0:
        print('Action denied: Reserve ratios must be above 4.0 to redeem reserve coins.')
        return

    total_reserves = new_total_reserves
    number_reserve_coins = new_number_reserve_coins
    return zeph_received

### situations
def situation_1():
    print('situation1 - Hardfork success and conversions are activated. Values initialized to 0')
    global total_reserves 
    global number_stable_coins
    global number_reserve_coins
    global spot
    global ma

    total_reserves = 0 # 0 ZEPH in reserve
    number_stable_coins = 0 # 0 ZUSD in circulation
    number_reserve_coins = 0 # 0 ZRSV in circulation
    spot = 2 # 1 ZEPH = $2
    ma = 1.5 # 1 ZEPH = $1.5

    #print starting values
    print_state()

    print('2. Mint 2000 ZRSV at price PminRC')

    tx_zeph_amount_spent = 1000
    rc_recevied = mint_reserve_coins(tx_zeph_amount_spent)
    print('rc_recevied: ', rc_recevied)

    print_state()

    print('3. Mint stable coins at the min of spot and MA.')

    tx_zeph_amount_spent = 300
    sc_received = mint_stable_coins(tx_zeph_amount_spent)
    print('sc_received: ', sc_received)

    print_state()

    print('4. Mint ZRSV for 200 ZEPH')

    tx_zeph_amount_spent = 200
    rc_recevied = mint_reserve_coins(tx_zeph_amount_spent)
    print('rc_recevied: ', rc_recevied)

    print_state()

    print('5. Redeem 200 reserve coins')

    tx_zrs_amount_spent = 200
    zeph_received = redeem_reserve_coins(tx_zrs_amount_spent)
    print('zeph_received: ', zeph_received)

    print_state()

    print('6. Redeem 250 stable coins')

    tx_zusd_amount_spent = 250
    zeph_received = redeem_stable_coins(tx_zusd_amount_spent)
    print('zeph_received: ', zeph_received)

    print_state()

    print('7. Redeem remaining stable coins')

    tx_zusd_amount_spent = number_stable_coins
    zeph_received = redeem_stable_coins(tx_zusd_amount_spent)
    print('zeph_received: ', zeph_received)

    print_state()

    print('8. Redeem remaining reserve coins')

    tx_zrs_amount_spent = number_reserve_coins
    zeph_received = redeem_reserve_coins(tx_zrs_amount_spent)
    print('zeph_received: ', zeph_received)

    print_state()


def situation_2():
    #worst case - reserve ratio < 1
    print('1. init state')
    global total_reserves 
    global number_stable_coins
    global number_reserve_coins
    global spot
    global ma

    total_reserves = 1000 # 0 ZEPH in reserve
    number_stable_coins = 500 # 0 ZUSD in circulation
    number_reserve_coins = 1000 # 0 ZRSV in circulation
    spot = 2 # 1 ZEPH = $2
    ma = 1.5 # 1 ZEPH = $1.5

    print_state()

    print('1. 100 stables are redeemed - reserve ratios (5.0,3.75)')

    tx_zusd_amount_spent = 100
    zeph_received = redeem_stable_coins(tx_zusd_amount_spent)
    print('\nzeph_received: ', zeph_received)
    print('received_dollar_value_spot: $', round(zeph_received * spot,2))
    print('received_dollar_value_ma: $', round(zeph_received * ma,2))

    print_state()

    print('2. spot price suddenly drops to $30c - reserve ratio < 1')

    spot = .3

    print_state()

    print('3. redeem 300 stable - worst case scenario, not enough reserves to cover. MA unaffected')

    tx_zusd_amount_spent = 300
    zeph_received = redeem_stable_coins(tx_zusd_amount_spent)
    print('\nzeph_received: ', zeph_received)
    print('received_dollar_value_spot: $', round(zeph_received * spot,2))
    print('received_dollar_value_ma: $', round(zeph_received * ma,2))

    print_state()

    print('4. redeem 200 stable - MA affected and = Spot')

    ma = .3

    print_state()

    tx_zusd_amount_spent = 100
    zeph_received = redeem_stable_coins(tx_zusd_amount_spent)
    print('\nzeph_received: ', zeph_received)
    print('received_dollar_value_spot: $', round(zeph_received * spot,2))
    print('received_dollar_value_ma: $', round(zeph_received * ma,2))

    print_state()


situation_1()
#situation_2()


