/*
Gavin Henderson
Oct 17, 2025
Abstract Classes and Polymorphism
*/


import javax.swing.JFrame;
import java.awt.Toolkit;


public class Game extends JFrame
{

	private boolean keepGoing; //whether or not the game is running
	private View view; //the view of the game
	private Model model; //the data of the game
	private Controller controller; //the controller of the game
	private Link link; //character user moves

	public static final int SCREEN_WIDTH = 700;
	public static final int SCREEN_HEIGHT = 500;
	public static final int WORLD_WIDTH = 1400; 
	public static final int WORLD_HEIGHT = 1000; 
	
	
	public Game()
	{


		model = new Model(); //the data of the game

		//laod the map from file upon startup
		String filename = "map.json";
		Json loadObject = Json.load(filename);
		model.unmarshal(loadObject);

		controller = new Controller(model); //handle input
		model.setController(controller); //give the model a reference to the controller
		view = new View(model); //gui panel to display 
		model.setView(view);
		controller.setView(view);


		
		this.setTitle("A4 - Abstract Classes and Polymorphism!"); //set the title of the window
		this.setSize(SCREEN_WIDTH, SCREEN_HEIGHT); //size the window
		this.setFocusable(true); //allow key/mouse input
		this.getContentPane().add(view); //add the view panel to the window
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setVisible(true); //show window
		keepGoing = true; //start the game running
		view.addMouseListener(controller); //add mouse listener to the view
		this.addKeyListener(controller); //add key listener to the view
	}

	public static void main(String[] args)
	{
		Game g = new Game(); //entry point. create the game
		g.run();
	}

	public void run()
	{
		do
		{
			link = model.getLink();//get correct link object
			link.setPX(link.getX());//store previous position
			link.setPY(link.getY());

			keepGoing = controller.update();	//check if we should keep running the game
			model.update(); //update the model
			view.repaint(); // This will indirectly call View.paintComponent
			Toolkit.getDefaultToolkit().sync(); // Updates screen

			// Go to sleep for 50 milliseconds
			try
			{
				Thread.sleep(50);
			} catch(Exception e) {
				e.printStackTrace();
				System.exit(1);
			}
		}
		while(keepGoing);
	}
}
