import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値:タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  #方横向
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  #縦方向
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数：スクリーンサーフェイス
    戻り値：なし
    接触時にGameOverを表示する
    """
    black_img = pg.Surface((WIDTH, HEIGHT))
    black_img.fill((0, 0, 0))  # 色指定
    black_img.set_alpha(180)

    fonto = pg.font.Font(None, 100)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 文字の位置

    over_img = pg.image.load("fig/8.png")
    cry_rect_left = over_img.get_rect(center=(WIDTH // 2 -250, HEIGHT // 2))  #ゲームオーバー時のこうかとんの位置
    cry_rect_right = over_img.get_rect(center=(WIDTH // 2 +250, HEIGHT // 2))



    #black_img.blit(txt, [300, 200])
    black_img.blit(txt, txt_rect)  #指定した位置に張り付ける
    
    black_img.blit(over_img, cry_rect_left)
    black_img.blit(over_img, cry_rect_right)


    screen.blit(black_img, [0,0])
    pg.display.update()
    time.sleep(5)  # 5秒間表示する
    
    
# get_kk_imgs() -> dict[tuple[int, int], pg.Surface]




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 練習2：空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  # 練習2：四隅の黒い部分を透過する
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    vx, vy = +5, +5  #練習2：爆弾の初期速度
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  #kkとbbのrectが重なっていたら
            print("game over")
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 練習2：横方向移動量
                sum_mv[1] += tpl[1]  # 練習2：縦方向移動量

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # どこかしらはみ出ている
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 反転
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  #練習2：爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1

        screen.blit(bb_img, bb_rct)  #練習2：爆弾表示

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
