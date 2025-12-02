/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/


import java.awt.Graphics;
import java.awt.image.BufferedImage;


public abstract class Sprite
{

    protected int x;
    protected int y;
    protected int h;
    protected int w;
    protected double speed;

    protected boolean update;



    public Sprite(int x, int y, int w, int h)
    {

        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h; 
    }

    public int getX(){
        return this.x;
    }

    public int getY(){
        return this.y;
    }

    public int getH(){
        return this.h;
    }

    public int getW(){
        return this.w;
    }

    public void setX(int x){
        this.x = x;
    }

    public void setY(int y){
        this.y = y;
    }

    public void setH(int h){
        this.h = h;
    }

    public void setW(int w){
        this.x = w;
    }

    public abstract void Draw(Graphics g, int scrollX, int scrollY);

    public abstract boolean update(Model model);

    public abstract Json marshal();

    public abstract void manageCollision(Sprite other);

    public abstract BufferedImage getImage();

    public abstract String toString();

    public Sprite collisionDetection(Sprite sprite){

        if (this != sprite){
            int otherLeft = sprite.getX();
            int otherRight = sprite.getX() + sprite.getW();
            int otherTop = sprite.getY();
            int otherBottom = sprite.getY() + sprite.getH();

            if (this.x + this.w > otherLeft && this.x < otherRight && this.y + this.h > otherTop && this.y < otherBottom){
                return sprite;
            }
            }


        return null;
    }

    public boolean isTree(){
        return false;
    }

    public boolean isTreasureChest(){
        return false;
    }

    public boolean isLink(){
        return false;
    }

    public boolean isBoomerang(){
        return false;
    }

}

