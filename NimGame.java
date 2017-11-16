import javax.swing.JFrame;

public class NimGame {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		JFrame frame = new JFrame("Nim Game");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		Interface init = new Interface();
		
		frame.getContentPane().add(init);
		frame.pack();
		frame.setVisible(true);
	}

}
