package edu.du.cs.aharrison.painter;
import java.awt.*;

public class Line extends PaintingPrimitive{
	Point startPoint, endPoint;
	Color color;
	Line(Color color, Point startPoint, Point endPoint) {
		super(color);
		this.startPoint = startPoint;
		this.endPoint = endPoint;
		this.color = color;
	}

	@Override
	protected void drawGeometry(Graphics g) {
		g.drawLine(startPoint.x, startPoint.y, endPoint.x, endPoint.y);
	}
	
}
