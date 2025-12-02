/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/

import java.util.ArrayList;

import javax.imageio.ImageIO;

import java.awt.image.BufferedImage;
import java.io.File;
import java.awt.Graphics;


public class Boomerang extends Sprite
{

    private static ArrayList<BufferedImage> boomerangImgs;
    private int frame = 0;
    private boolean alive = true;

    private double speed = 15.0;
    private String direction;

    public Boomerang(int x, int y, String direction){
        super(x, y, 20, 20);
        this.direction = direction;

        if (boomerangImgs == null){
            boomerangImgs = new ArrayList<BufferedImage>();
            for (int i = 1; i <= 4; i++){
                String filename = "images/boomerang" + i + ".png";
                try{
                    boomerangImgs.add(ImageIO.read(new File(filename)));
                }
                catch(Exception e){
                    e.printStackTrace(System.err);
                    System.exit(1);
                }
            }
        }
        
    }

    //getters and setters for boomerang
    public static ArrayList<BufferedImage> getBoomerangImgs(){
        return boomerangImgs;
    }

    public double getSpeed(){
        return speed;
    }


    @Override
    public void Draw(Graphics g, int scrollX, int scrollY){
        BufferedImage boomerangImg = boomerangImgs.get(this.frame);
        if (boomerangImg != null){
            g.drawImage(boomerangImg, this.x - scrollX, this.y - scrollY, this.w, this.h, null);
        }
    }

    @Override
    public boolean update(Model model){
        if (this.direction == "up"){
            this.y -= speed;
        }
        else if (this.direction == "down"){
            this.y += speed;
        }
        else if (this.direction == "left"){
            this.x -= speed;
        }
        else if (this.direction == "right"){
            this.x += speed;
        }
        this.updateFrame();
        return alive;
        }

    @Override
    public void manageCollision(Sprite other){
        if (other.isTree() || other.isTreasureChest()){
            this.alive = false;
        }
    }

    @Override
    public BufferedImage getImage(){
        return boomerangImgs.get(this.frame);
    }

    public void updateFrame(){
        this.frame = (this.frame + 1) % 4;
    }

    @Override
    public Json marshal(){
        return null;
    }

    @Override
    public String toString()
    {
        return "Boomerang (x,y) = (" + x + ", " + y + "), w = " + w + ", h = " + h + ", direction = " + direction + ", speed = " + speed;
    }
    

    @Override
    public boolean isBoomerang(){
        return true;
    }



}