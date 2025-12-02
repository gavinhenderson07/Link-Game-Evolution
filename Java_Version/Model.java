/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/

import java.util.ArrayList;
import java.util.Iterator;

public class Model
{
	
	private ArrayList<Sprite> sprites;
	private ArrayList<Sprite> canAdd;
	private int itemIndex = 0;
	private Link link;
	private Controller controller;
	private View view;
	private TreasureChest chest;

	private boolean editMode = false;
	private boolean addItem = true;

	private String direction;

    //constructor
	public Model()
    {
        //model constructor
		this.sprites = new ArrayList<Sprite>();
		this.link = new Link();
		this.sprites.add(this.link);

		//create a treasure chest and a tree to add in edit mode
		this.chest = new TreasureChest(-100, -100);
		Tree tree = new Tree(-100, -100);

		this.canAdd = new ArrayList<Sprite>();
		this.canAdd.add(tree);
		this.canAdd.add(chest);
		
		
	}

	public void setView(View v){
		this.view = v;
	}

	public void setController(Controller c){
		this.controller = c;
	}

	public void update()
	{
		//chaeck for collisions between sprites

		Iterator<Sprite> it = sprites.iterator();
		while (it.hasNext()){
			Sprite curr1 = it.next();

			boolean stillValid = curr1.update(this);
			if(!stillValid){
				it.remove();
				continue;
			}

			Iterator<Sprite> it2 = sprites.iterator();
			while (it2.hasNext()){
				Sprite curr2 = it2.next();
				if (curr1 != curr2){
					if(curr1.collisionDetection(curr2) != null){
						curr1.manageCollision(curr2);
						curr2.manageCollision(curr1);
					}
				}
			}
		}


			
		
		//handle the scrolling of the view if link goes to the map edge
		int rightScreenEdge = view.getScrollX() + Game.SCREEN_WIDTH;
		int leftScreenEdge = view.getScrollX();
		int topScreenEdge = view.getScrollY();
		int bottomScreenEdge = view.getScrollY() + Game.SCREEN_HEIGHT;

		if (controller.isRightPressed() && link.getX() + link.getW() > rightScreenEdge){
			if (view.getScrollX() < Game.WORLD_WIDTH - Game.SCREEN_WIDTH){
				view.setScroll(view.getScrollX() + Game.SCREEN_WIDTH, view.getScrollY());

				link.setX(view.getScrollX() + 5);
			}
			}else if(controller.isLeftPressed() && link.getX() < leftScreenEdge){
				if (view.getScrollX() > 0){
					view.setScroll(view.getScrollX() - Game.SCREEN_WIDTH, view.getScrollY());

					link.setX(Game.SCREEN_WIDTH - link.getW() - 12);
				}
			}else if(controller.isDownPressed() && link.getY() + link.getH() > bottomScreenEdge){
				if (view.getScrollY() < Game.WORLD_HEIGHT - Game.SCREEN_HEIGHT){
					view.setScroll(view.getScrollX(), view.getScrollY() + Game.SCREEN_HEIGHT);

					link.setY(view.getScrollY() + 5);
				}
			}else if(controller.isUpPressed() && link.getY() < topScreenEdge){
				if (view.getScrollY() > 0){
					view.setScroll(view.getScrollX(), view.getScrollY() - Game.SCREEN_HEIGHT);

					link.setY(Game.SCREEN_HEIGHT - link.getH() - 25);
				}
			}
	}

	//trees getter
	public ArrayList<Sprite> getSprites(){
		return this.sprites;
	}

	//item index getter/setter
	public int getItemIndex(){
		return this.itemIndex;
	}
	
	public Sprite getCurrItem(){
		return this.canAdd.get(this.itemIndex);
	}

	public void setItemIndex(){
		//0 is tree, 1 is chest
		this.itemIndex = (this.itemIndex + 1) % this.canAdd.size();
	}
	
	//add tree function
	public void addSprite(int x, int y){
		Sprite toAdd = this.getCurrItem();

		if (toAdd.isTree()){
			int snappedX = Math.floorDiv(x, 75) * 75;
			int snappedY = Math.floorDiv(y, 75) * 75;
			if (!this.isSpriteAt(snappedX, snappedY)){
				this.sprites.add(new Tree(snappedX, snappedY));
			}
		}
		else if (toAdd.isTreasureChest()){
			int centeredX = x - toAdd.getW()/2;
			int centeredY = y - toAdd.getH()/2;

			//create temp chest to check for collisions
			TreasureChest temp = new TreasureChest(centeredX, centeredY);

			//check for collison before adding
			if (!this.isAreaColliding(temp)){
				//add the temp if no collision
				this.sprites.add(temp);
			}

		}
	}

	private boolean isAreaColliding(Sprite s){
		for (Sprite sprite: this.sprites){
			if (s.collisionDetection(sprite) != null){
				return true;
			}
		}
		return false;
	}

	//clearing trees
	public void clearAllTrees(){

		Iterator<Sprite> it = sprites.iterator();
		while (it.hasNext()){
			Sprite curr = it.next();
			if (curr.isTree() || curr.isTreasureChest()){
				it.remove();
			}
		}
	}

	//check is a sprite is at a x,y position
	public boolean isSpriteAt(int x, int y){
		for (int i = 0; i < sprites.size(); i++){
			Sprite t = sprites.get(i);
			if (t.isTree() || t.isTreasureChest()){
				if (t.getX() == x && t.getY() == y){
					return true;
				}
			}
		}
		return false;
	}

	//link getter
	public Link getLink(){
		return this.link;
	}

	//remove tree at location
	public void removeSprite(int x, int y){
		for (int i = 0; i < sprites.size(); i++){
			Sprite t = sprites.get(i);
			if (t.getClass() ==  this.getCurrItem().getClass()){
				if (x >= t.getX() && x <= t.getX() + t.getW() && y >= t.getY() && y <= t.getY() + t.getH()){
					sprites.remove(i);
					return;
				}
			}
		}
	}


	//marshal to json
	public Json marshal(){
		Json ob = Json.newObject();
		Json spriteArray = Json.newList();

		for (int i = 0; i < this.sprites.size(); i++){
				Sprite t = this.sprites.get(i);
				if (t.isTree() || t.isTreasureChest()){
					spriteArray.add(t.marshal());
				}
		}
		ob.add("sprites", spriteArray);
		return ob;
	}

	//unmarshal from json
	public void unmarshal(Json ob){
		this.clearAllTrees();
		Json treeArray = ob.get("sprites");
		for (int i = 0; i < treeArray.size(); i++){
			Json treeOb = treeArray.get(i);
			String type = treeOb.getString("type");
			if (type.equals("TreasureChest")){
				TreasureChest tc = new TreasureChest(0, 0);
				tc.unmarshal(treeOb);
				this.sprites.add(tc);
			}
			else if (type.equals("tree")){
				Tree t = new Tree(0,0);
				t.unmarshal(treeOb);
				this.sprites.add(t);
			}
		}
	}


	//edit mode changers
	public boolean getEditMode(){
		return this.editMode;
	}

	public boolean getAddItem(){
		return this.addItem;
	}

	public void toggleEditMode(){
		this.editMode = !this.editMode;
	}

	public void setAddItem(boolean val){
		this.addItem = val;
	}

	//direction setters and getters
	public String getDirection(){
		return this.direction;
	}

	public void setDirection(String dir){
		this.direction = dir;
	}

	//controller calls these based on key input
	public void moveUp(){
		this.link.moveUp();
	}
	public void moveDown(){
		this.link.moveDown();
	}
	public void moveLeft(){
		this.link.moveLeft();
	}
	public void moveRight(){
		this.link.moveRight();
	}
	public void stopMoving(){
		this.link.resetFrame();
	}

	//create method for throwing boomerang
	public void throwBoomerang(){
		//create new boomerang for link to throw from center of link
		int linkCenterX = this.link.getX() + this.link.getW()/2;
		int linkCenterY = this.link.getY() + this.link.getH()/2;

		int boomX = linkCenterX - 10; //boomerang width is 20, so offset by 10
		int boomY = linkCenterY - 10; //offset by 10

		Boomerang b = new Boomerang(boomX, boomY, this.link.getDirection());
		this.sprites.add(b);
	}
}