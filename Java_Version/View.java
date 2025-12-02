/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/

import javax.swing.JPanel;
import java.awt.Graphics;


import java.awt.Color;


public class View extends JPanel
{
	
	private Model model;

	private int scrollX = 0;
	private int scrollY = 0;

	//link animation images
	

	public View(Model m)
	{
		this.model = m;

	}

	//removes the button from the panel
	public void removeButton()
	{}

	//called whenever the panel needs to be redrawn
	public void paintComponent(Graphics g)
	{
		g.setColor(new Color(72, 152, 72));
		g.fillRect(0, 0, this.getWidth(), this.getHeight());

		for (Sprite sprite: model.getSprites()){
			sprite.Draw(g, scrollX, scrollY);
		}

		if (model.getEditMode()){
			if (model.getAddItem() == true){
				g.setColor(new Color(72, 152, 72).darker());
			}
			else{
				g.setColor(new Color(204, 51, 51));
			}

			g.fillRect(0, 0, 100, 100);
			Sprite currItem = model.getCurrItem();
			if (currItem.isTreasureChest()){
				g.drawImage(currItem.getImage(), 10, 10, 80, 80, null);
			}
			else if (currItem.isTree()){
				g.drawImage(currItem.getImage(), 10, 10, 80, 80, null);
			}
		}



	}



	public int getScrollX(){
		return this.scrollX;
	}
	
	public int getScrollY(){
		return this.scrollY;
	}

	public void setScroll(int x, int y){
		this.scrollX = x;
		this.scrollY = y;
	}
}


