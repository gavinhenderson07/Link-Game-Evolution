/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/

import java.util.ArrayList;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import java.awt.Graphics;


public class Link extends Sprite
{


    private int px;
    private int py;

    int frame = 0;
    String direction = "down";

    private static ArrayList<BufferedImage> linkDown;
    private static ArrayList<BufferedImage> linkUp;
    private static ArrayList<BufferedImage> linkRight;
    private static ArrayList<BufferedImage> linkLeft;


    public Link(){
        //set default values
        //calling parent constructor
        super(100, 100, 40, 50);
        this.speed = 10.0;
        

        //load in link walking animations
        if (linkDown == null){
            try{
                linkDown = new ArrayList<BufferedImage>();
                for (int i = 1; i <= 5; i++){
                    String filename = "images/link" + i + ".png";
                    linkDown.add(ImageIO.read(new File(filename)));
                }

            
                //load in link walking frames left
                linkLeft = new ArrayList<BufferedImage>();
                for (int i = 12; i <= 16; i++){
                    String filename = "images/link" + i + ".png";
                    linkLeft.add(ImageIO.read(new File(filename)));
                }

                //load in link walking frames right
                linkRight = new ArrayList<BufferedImage>();
                for (int i = 23; i <= 27; i++){
                    String filename = "images/link" + i + ".png";
                    linkRight.add(ImageIO.read(new File(filename)));
                }

                //load in link walking frames up
                linkUp = new ArrayList<BufferedImage>();
                for (int i = 34; i <= 38; i++){
                    String filename = "images/link" + i + ".png";
                    linkUp.add(ImageIO.read(new File(filename)));
                }
            }
            catch(Exception e)
            {
                e.printStackTrace(System.err);
                System.exit(1);
            }
        }

    }


    @Override
    public void Draw(Graphics g, int scrollX, int scrollY){
        BufferedImage link_img = null;
        	switch(this.direction){
			case "down":
				link_img = linkDown.get(this.frame);
				break;
			case "up":
				link_img = linkUp.get(this.frame);
				break;
			case "left":
				link_img = linkLeft.get(this.frame);
				break;
			case "right":
				link_img = linkRight.get(this.frame);
				break;
		}

        
        if (link_img != null){
            g.drawImage(link_img, this.x - scrollX, this.y - scrollY, this.w, this.h, null);
        }

    }

    @Override
    public BufferedImage getImage(){
        BufferedImage link_img = null;
        switch(this.direction){
            case "down":
                link_img = linkDown.get(this.frame);
                break;
            case "up":
                link_img = linkUp.get(this.frame);
                break;
            case "left":
                link_img = linkLeft.get(this.frame);
                break;
            case "right":
                link_img = linkRight.get(this.frame);
                break;
        }
        return link_img;
    }


    //link getters and setters

    public int getPX(){
        return this.px;
    }

    public int getPY(){
        return this.py;
    }

    public double getSpeed(){
        return this.speed;
    }

    public String getDirection(){
        return this.direction;
    }

    public int getFrame(){
        return this.frame;
    }

    public void setDirection(String dir){
        this.direction = dir;
    }

    public void setX(int x){
        this.x = x;
    }

    public void setY(int y){
        this.y = y;
    }

    public void setPX(int px){
        this.px = px;
    }

    public void setPY(int py){
        this.py = py;
    }

    //change fram as needed
    public void updateFrame(){
        this.frame = (this.frame + 1) % 5;
    }

    //set frame to 0 when not moving
    public void resetFrame(){
        this.frame = 0;
    }

    //movement functions for link

    public void moveUp(){
        this.setDirection("up");
        this.setY(this.y - (int)this.speed);
        this.updateFrame();
    }

    public void moveDown(){
        this.setDirection("down");
        this.setY(this.y + (int)this.speed);
        this.updateFrame();
    }

    public void moveLeft(){
        this.setDirection("left");
        this.setX(this.x - (int)this.speed);
        this.updateFrame();
    }

    public void moveRight(){
        this.setDirection("right");
        this.setX(this.x + (int)this.speed);
        this.updateFrame();
    }

    @Override
    public void manageCollision(Sprite t){

        
        //move link back to previous position in case of collision
        if (t.isTree()){
            int linkPrevRight = this.px + this.w;
            int linkPrevLeft = this.px;
            int linkPrevTop = this.py;
            int linkPrevBottom = this.py + this.h;

            if (linkPrevRight <= t.getX()){
                this.x = (t.getX() - this.w);
            }
            else if (linkPrevLeft >= t.getX() + t.getW()){
                this.x = (t.getX() + t.getW());
            }
            else if (linkPrevBottom <= t.getY()){
                this.y = (t.getY() - this.h);
            }
            else if (linkPrevTop >= t.getY() + t.getH()){
                this.y = (t.getY() + t.getH());
            }   
        }

        if (t.isTreasureChest()){
            TreasureChest tc = TreasureChest.class.cast(t);
            if (tc.getOpened() == true){
                if (tc.getCountdown() <= 75){
                    return;
                }
                this.x = this.px;
                this.y = this.py;
            }
        }
    }

    @Override
    public boolean update(Model model)
    {
    //future logic goes here
    return true;
    }

    @Override
    public Json marshal()
    {
        return null;
    }


    @Override
    public String toString() 
    {
        return "Link is at (" + this.x + ", " + this.y + ") facing " + this.direction + " on frame " + this.frame;
    }

    @Override
    public boolean isLink(){
        return true;
    }



}