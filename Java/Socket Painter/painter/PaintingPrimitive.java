package edu.du.cs.aharrison.painter;
import java.awt.Color;
import java.awt.Graphics;
import java.io.Serializable;

public abstract class PaintingPrimitive implements Serializable{
	
	Color color;
	PaintingPrimitive(Color color){
		this.color = color;
	}
	
	public final void draw(Graphics g) {
	    g.setColor(this.color);
	    drawGeometry(g);
	}
	
	protected abstract void drawGeometry(Graphics g);

}
