import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  # 練習３：押下キーと移動量の辞書
    pg.K_UP: (0, -5),  # キー：移動量／値：（横方向移動量，縦方向移動量）
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向，縦方向はみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return yoko, tate



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img2 =pg.image.load("ex02/fig/8.png")
    kk_lst = {}
    kk_lst[(0,0)] = pg.transform.flip(kk_img,True,False)
    kk_lst[(0,5)] = pg.transform.flip(pg.transform.rotate(kk_img,90),True, False)
    kk_lst[(5,5)] = pg.transform.flip(pg.transform.rotate(kk_img,45),True, False)
    kk_lst[(5,0)] = pg.transform.flip(pg.transform.rotate(kk_img,0),True, False)
    kk_lst[(5,-5)] = pg.transform.flip(pg.transform.rotate(kk_img,-45),True, False)
    kk_lst[(0,-5)] = pg.transform.flip(pg.transform.rotate(kk_img,-90),True, False)
    kk_lst[(-5,-5)] = pg.transform.rotate(kk_img,-45)
    kk_lst[(-5,0)] = pg.transform.rotate(kk_img,0)
    kk_lst[(-5,5)] = pg.transform.rotate(kk_img,45)
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img2 = pg.transform.rotozoom(kk_img2, 0, 2.0)
    kk_rct = kk_img.get_rect()  # 練習３：こうかとんSurfaceのRectを抽出する
    kk_rct.center = 900, 400  # 練習３：こうかとんの初期座標
    bb_img = pg.Surface((20, 20))   # 練習１：透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  # 練習１：黒い部分を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習１：赤い半径10の円を描く
    bb_rct = bb_img.get_rect()  # 練習１：爆弾SurfaceのRectを抽出する
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    time = 0
    time2 = 1
    vx, vy = 0,0  # 練習２：爆弾の速度
    tmr = 0
    vxx = 1
    vyy = 1
    do=True
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            do = False
            if not do:
                print("Game Over")
                screen.blit(kk_img2,kk_rct)
                pg.display.update()

        if do:   
            key_lst = pg.key.get_pressed()
            sum_mv = [0, 0]
            for k, tpl in delta.items():
                if key_lst[k]:  # キーが押されたら
                    sum_mv[0] += tpl[0]
                    sum_mv[1] += tpl[1]
            
            screen.blit(bg_img, [0, 0])
            kk_rct.move_ip(sum_mv[0], sum_mv[1])
            if check_bound(kk_rct) != (True, True):
                kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

            screen.blit(kk_lst[tuple(sum_mv)], kk_rct)  # 練習３：こうかとんを移動させる
            if time2 <10:
                vx = (time2)*vxx
                vy = (time2)*vyy

            elif time2>=10:
                vx = 10*vxx
                vy = 10*vyy

            yoko, tate = check_bound(bb_rct)
            if not yoko:  # 横方向にはみ出たら
                vx *= -1
                vxx *=-1

            if not tate:  # 縦方向にはみ出たら
                vy *= -1
                vyy *=-1
                
            bb_rct.move_ip(vx,vy) 
            screen.blit(bb_img, bb_rct)
            pg.display.update()
            print(vx)
            tmr += 1
            time +=1
            if time % 100 == 99:
                time2 += 1


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()