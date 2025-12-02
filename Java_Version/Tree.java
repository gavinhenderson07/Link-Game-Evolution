/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/

import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import java.awt.Graphics;




public class Tree extends Sprite
{

    

    private static BufferedImage tree_img;



    public Tree(int x, int y){

        //call the parent constructor
        super(x, y, 60, 75);

        if (tree_img == null){
            try{
                tree_img = ImageIO.read(new File("images/tree.png"));
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
        g.drawImage(tree_img, this.x - scrollX, this.y - scrollY,this.w, this.h, null);

        //g.setColor(Color.BLUE);
        //g.drawRect(this.x - scrollX, this.y - scrollY, this.w, this.h);
    }

    //getters and setters for tree
    @Override
    public BufferedImage getImage(){
        return tree_img;
    }


    //marshal and unmarshal functions
    @Override
    public Json marshal(){
        Json ob = Json.newObject();
        ob.add("x", this.x);
        ob.add("y", this.y);
        ob.add("w", this.w);
        ob.add("h", this.h);
        ob.add("type", "tree");
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
	    return "Tree (x,y) = (" + x + ", " + y + "), w = " + w + ", h = " + h;
    }

    @Override
    public boolean update(Model model){return true;}

    @Override
    public void manageCollision(Sprite other){
        //trees dont need this
    }

    @Override
    public boolean isTree(){
        return true;
    }
}