package edu.du.cs.aharrison.painter;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import javax.swing.JPanel;

public class PaintingPanel extends JPanel {
	ArrayList<PaintingPrimitive> primitives = new ArrayList<PaintingPrimitive>();
	PaintingPanel(){
		setBackground(Color.WHITE);
	}
	
	public void addPrimitive(PaintingPrimitive obj) {
		//System.out.println("addPrimitive");
        this.primitives.add(obj);
        this.repaint();
}
	
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		//System.out.println("paintComponent");
		 for(PaintingPrimitive obj : primitives) {
			 obj.draw(g);
		 }
	}

}	
