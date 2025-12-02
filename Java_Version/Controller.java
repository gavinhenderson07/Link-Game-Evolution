/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/

import java.awt.event.MouseListener;
import java.awt.event.MouseEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyListener;
import java.awt.event.KeyEvent;

public class Controller implements ActionListener, MouseListener, KeyListener
{
	private boolean keepGoing; //game to continue running
	private View view; //reference to view
	private Model model; //reference to model

	private boolean keyLeft;
	private boolean keyRight;
	private boolean keyUp;
	private boolean keyDown;

	private boolean editMode = false;
	private boolean addItem = true;
	
	
	public Controller(Model m)
	{
		model = m;
		keepGoing = true; //start the game running
	}

	//called when the button is clicked
	public void actionPerformed(ActionEvent e)
	{

		
	}

	//returns whether game is running or not
	public boolean update()
	{	
		if (this.keyUp){
			model.moveUp();
		}
		else if (this.keyDown){
			model.moveDown();
		}
		else if (this.keyLeft){
			model.moveLeft();
		}
		else if (this.keyRight){
			model.moveRight();
		}
		else if (!this.keyUp && !this.keyDown && !this.keyLeft && !this.keyRight){
			model.stopMoving();
		}
		return keepGoing;
	}

	

	//give the controller a reference to the view
	public void setView(View v)
	{
		view = v;
	}

	//called when the mouse is pressed
	public void mousePressed(MouseEvent e)
	{	

		if (model.getEditMode() == true){
			int currX = view.getScrollX();
			int currY = view.getScrollY();

			if (e.getX() < 100 && e.getY() < 100){
				model.setItemIndex();
				return;
			}
			else if (model.getAddItem() == true){
				int x = e.getX() + currX;
				int y = e.getY() + currY;
				
				model.addSprite(x, y);
			}
			else if (model.getAddItem() == false){
				model.removeSprite(e.getX() + currX, e.getY() + currY);
			}
		
		}

	}

	public void mouseReleased(MouseEvent e) {}
	public void mouseEntered(MouseEvent e) {}
	public void mouseExited(MouseEvent e) {}
	public void mouseClicked(MouseEvent e) {}

	//key listener methods
	public void keyPressed(KeyEvent e)
	{
		switch(e.getKeyCode())
		{
			case KeyEvent.VK_RIGHT: 
				keyRight = true; 
				break;
			case KeyEvent.VK_LEFT: 
				keyLeft = true; 
				break;
			case KeyEvent.VK_UP: 
				keyUp = true; 
				break;
			case KeyEvent.VK_DOWN: 
				keyDown = true; 
				break;
			case KeyEvent.VK_SPACE:
				model.throwBoomerang();
				break;
	}


	}

	//called when a key is released
	public void keyReleased(KeyEvent e)
	{
		switch(e.getKeyCode())
		{
			case KeyEvent.VK_RIGHT:
				keyRight = false; 
				break;
			case KeyEvent.VK_LEFT: 
				keyLeft = false; 
				break;
			case KeyEvent.VK_UP: 
				keyUp = false; 
				break;
			case KeyEvent.VK_DOWN: 
				keyDown = false; 
				break;
			case KeyEvent.VK_ESCAPE:
				System.exit(0);
		}
		char c = Character.toLowerCase(e.getKeyChar());
		if(c == 'q')
			System.exit(0);

		if (c == 'e'){
			model.toggleEditMode();
			model.setAddItem(true);
		}
		if (c == 'a' && model.getEditMode()){
			model.setAddItem(true);
		}

		if (c == 'r' && model.getEditMode()){
			model.setAddItem(false);
		}

		if (c == 'c' && model.getEditMode()){
			model.clearAllTrees();
		}


		String filename = "map.json";
		switch (c) {
			/*case 'l' :
				Json loadObject = Json.load(filename);
				model.unmarshal(loadObject);
				System.out.println("file " + filename + "loaded!");
				break;*/
			case 's' :
				Json saveObject = model.marshal();
				saveObject.save(filename);
				System.out.println("saved " + filename + "file!");
				break;
			case 'q':
				keepGoing = false;
		}
		


	}

	public void keyTyped(KeyEvent e)
	{  
		
	}

	public boolean getEditMode(){
		return this.editMode;
	}

	public boolean getAddItem(){
		return this.addItem;
	}

	public boolean isUpPressed(){
		return this.keyUp;
	}

	public boolean isDownPressed(){
		return this.keyDown;
	}

	public boolean isLeftPressed(){
		return this.keyLeft;
	}

	public boolean isRightPressed(){
		return this.keyRight;
	}
	
}


