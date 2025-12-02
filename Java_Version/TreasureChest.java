/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/

import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.File;

import javax.imageio.ImageIO;

public class TreasureChest extends Sprite{

    private boolean opened;
    private int countdown;
    private static BufferedImage closedImage;
    private static BufferedImage openedImage;

    public TreasureChest(int x, int y){
        super(x, y, 40, 40);
        this.opened = false;
        this.countdown = 0;

        if (closedImage == null){
            try{
                closedImage = ImageIO.read(new File("images/treasurechest.png"));
                openedImage = ImageIO.read(new File("images/rupee.png"));
            }
            catch(Exception e)
            {
                e.printStackTrace(System.err);
                System.exit(1);
            }
        }
    }


    public boolean getOpened(){
        return this.opened;
    }

    public int getCountdown(){
        return this.countdown;
    }

    public BufferedImage getImage(){
        return closedImage;
    }

    @Override
    public void Draw(Graphics g, int scrollX, int scrollY){
        //draw the chest
        if (this.opened){
            g.drawImage(openedImage, this.x - scrollX, this.y - scrollY, this.w, this.h, null);
        }
        else{
            g.drawImage(closedImage, this.x - scrollX, this.y - scrollY, this.w, this.h, null);
        }
    }

    @Override
    public boolean update(Model model){
        if (this.opened){
            this.countdown--;
            if (this.countdown <= 0){
                return false;
            }
        }
        return true;
    }

    @Override
    public void manageCollision(Sprite other){
        if (other.isLink() || other.isBoomerang()){
            if (this.opened == false){
                this.opened = true;
                this.countdown = 80; //timer for vanishing
            }
            else{
                if (countdown <= 75){
                    if (other.isLink() || other.isBoomerang()){
                        this.countdown = 1;//rubee vanishes next frame
                    }
                }
            }
        }
    }

    @Override
    public Json marshal(){
        Json ob = Json.newObject();
        ob.add("x", this.x);
        ob.add("y", this.y);
        ob.add("w", this.w);
        ob.add("h", this.h);
        ob.add("type", "TreasureChest");
        return ob;
    }

    public void unmarshal(Json ob){
        this.x = (int)ob.getLong("x");
        this.y = (int)ob.getLong("y");
        this.w = (int)ob.getLong("w");
        this.h = (int)ob.getLong("h");
    }

    @Override
    public String toString()
    {
        return "TreasureChest (x,y) = (" + x + ", " + y + "), w = " + w + ", h = " + h + ", opened = " + opened + ", countdown = " + countdown;
    }

    @Override
    public boolean isTreasureChest(){
        return true;
    }







}