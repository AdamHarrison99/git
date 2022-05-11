package edu.du.cs.aharrison.painter;
import java.awt.*;

public class Circle extends PaintingPrimitive{
	Point startPoint, radiusPoint;
	Color color;
	Circle(Color color, Point startPoint, Point radiusPoint) {
		super(color);
		this.startPoint = startPoint;
		this.radiusPoint = radiusPoint;
		this.color = color;
	}
	
	@Override
	protected void drawGeometry(Graphics g) {
		int radius = (int) Math.abs(startPoint.distance(radiusPoint));
        g.drawOval(startPoint.x - radius, startPoint.y - radius, radius*2, radius*2);
	}

}
