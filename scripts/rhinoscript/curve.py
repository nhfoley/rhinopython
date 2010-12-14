import scriptcontext
import utility as rhutil
import Rhino
import math
import System.Guid
import System.Array
import System.Enum

def AddArc(plane, radius, angle_degrees):
    """
    Adds an arc curve to the document
    Parameters:
      plane = the plane on which the arc will lie. The origin of the plane
              will be the center point of the arc. The x-axis of the plane
              defines the 0 angle direction.
      radius = radius of the arc
      angle_degrees = interval of arc
    Returns:
      id of the new curve object
      None on error  
    """
    plane = rhutil.coerceplane(plane)
    if( plane==None ): return scriptcontext.errorhandler()
    radians = math.radians(angle_degrees)
    arc = Rhino.Geometry.Arc(plane, radius, radians)
    rc = scriptcontext.doc.Objects.AddArc(arc)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddArc3Pt(start, end, point_on_arc):
    """
    Adds a 3-point arc curve to the document
    Parameters:
      start, end = endpoints of the arc
      point_on_arc = a point on the arc
    Returns:
      id of the new curve object if successful
      None on error
    """
    start = rhutil.coerce3dpoint(start)
    end = rhutil.coerce3dpoint(end)
    pton = rhutil.coerce3dpoint(point_on_arc)
    if( start==None or end==None or pton==None ):
        return scriptcontext.errorhandler()
    arc = Rhino.Geometry.Arc(start, end, pton)
    rc = scriptcontext.doc.Objects.AddArc(arc)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddArcPtTanPt(start, direction, end):
    """
    Adds an arc curve, created from a start point, a start direction, and an
    end point, to the document
    Returns:
      id of the new curve object if successful
      None on error
    """
    start = rhutil.coerce3dpoint(start)
    direction = rhutil.coerce3dvector(direction)
    end = rhutil.coerce3dpoint(end)
    if( start==None or direction==None or end==None ):
        return scriptcontext.errorhandler()
    arc = Rhino.Geometry.Arc(start, direction, end)
    rc = scriptcontext.doc.Objects.AddArc(arc)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddCircle( plane_or_center, radius ):
    """
    Adds a circle curve to the document
    Parameters:
      planeOrCenter = plane on which the circle will lie. If a point is
          passed, this will be the center of the circle on the active
          construction plane
      radius = the radius of the circle
    Returns:
      id of the new curve object if successful
      None on error
    """
    rc = None
    plane = rhutil.coerceplane(plane_or_center)
    if plane:
        circle = Rhino.Geometry.Circle(plane, radius)
        rc = scriptcontext.doc.Objects.AddCircle(circle)
        if( rc == System.Guid.Empty ): rc = None
    else:
        center = rhutil.coerce3dpoint(plane_or_center)
        if center:
            view = scriptcontext.doc.Views.ActiveView
            plane = view.ActiveViewport.ConstructionPlane()
            plane.Origin = center
            circle = Rhino.Geometry.Circle(plane, radius)
            rc = scriptcontext.doc.Objects.AddCircle(circle)
            if( rc == System.Guid.Empty ): rc = None
    if( rc==None ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddCircle3Pt(first, second, third):
    """
    Adds a 3-point circle curve to the document
    Parameters:
      first, second, third = points on the circle
    Returns:
      id of the new curve object if successful
      None on error
    """
    start = rhutil.coerce3dpoint(first)
    end = rhutil.coerce3dpoint(second)
    third = rhutil.coerce3dpoint(third)
    if( start==None or end==None or third==None ):
        return scriptcontext.errorhandler()
    circle = Rhino.Geometry.Circle(start, end, third)
    rc = scriptcontext.doc.Objects.AddCircle(circle)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddCurve( points, degree=3 ):
    """
    Adds a control points curve object to the document
    Parameters:
      points = a list of points
      degree [opt] = degree of the curve
    Returns:
      id of the new curve object if successful
      None on error
    """
    points = rhutil.coerce3dpointlist(points)
    if( points==None ): return scriptcontext.errorhandler()
    curve = Rhino.Geometry.Curve.CreateControlPointCurve(points, degree)
    if( curve==None ): return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddCurve(curve)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddEllipse( plane, radiusX, radiusY ):
    """
    Adds an elliptical curve to the document
    Parameters:
      plane = the plane on which the ellipse will lie. The origin of
              the plane will be the center of the ellipse
      radiusX, radiusY = radius in the X and Y axis directions
    Returns:
      id of the new curve object if successful
      None on error
    """
    plane = rhutil.coerceplane(plane)
    if( plane==None ): return scriptcontext.errorhandler()
    ellipse = Rhino.Geometry.Ellipse(plane, radiusX, radiusY)
    rc = scriptcontext.doc.Objects.AddEllipse(ellipse)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddEllipse3Pt( center, second, third ):
    """
    Adds a 3-point elliptical curve to the document
    Parameters:
      center = center point of the ellipse
      second = end point of the x axis
      third  = end point of the y axis
    Returns:
      id of the new curve object if successful
      None on error
    """
    center = rhutil.coerce3dpoint(center)
    second = rhutil.coerce3dpoint(second)
    third = rhutil.coerce3dpoint(third)
    if( center==None or second==None or third==None ):
        return scriptcontext.errorhandler()
    ellipse = Rhino.Geometry.Ellipse(center, second, third)
    rc = scriptcontext.doc.Objects.AddEllipse(ellipse)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddFilletCurve( curve0id, curve1id, radius=1.0, base_point0=None, base_point1=None ):
    """
    Adds a fillet curve between two curve objects
    Parameters:
      curve0id = identifier of the first curve object
      curve1id = identifier of the second curve object
      radius [opt] = fillet radius
      base_point0 [opt] = base point of the first curve. If omitted,
                          starting point of the curve is used
      base_point1 [opt] = base point of the second curve. If omitted,
                          starting point of the curve is used
    Returns:
      id of the new curve object if successful
      None on error
    """
    base0 = rhutil.coerce3dpoint(base_point0)
    if (base0==None): base0 = Rhino.Geometry.Point3d.Unset
    base1 = rhutil.coerce3dpoint(base_point1)
    if (base1==None ): base1 = Rhino.Geometry.Point3d.Unset

    curve0 = rhutil.coercecurve(curve0id)
    curve1 = rhutil.coercecurve(curve1id)
    if( curve0==None or curve1==None ): return scriptcontext.errorhandler()
    
    crv0_t = 0.0
    if(base0==Rhino.Geometry.Point3d.Unset):
        crv0_t = curve0.Domain.Min
    else:
        rc, t = curve0.ClosestPoint(base0, 0.0)
        if not rc: return scriptcontext.errorhandler()
        crv0_t = t
    crv1_t = 0.0
    if(base1==Rhino.Geometry.Point3d.Unset):
        crv1_t = curve1.Domain.Min
    else:
        rc, t = curve1.ClosestPoint(base1, 0.0)
        if not rc: return None
        crv1_t = t

    arc = Rhino.Geometry.Curve.CreateFillet(curve0, curve1, radius, crv0_t, crv1_t)
    rc = scriptcontext.doc.Objects.AddArc(arc)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddInterpCrvOnSrf( surface_id, points ):
    """
    Adds an interpolated curve object that lies on a specified surface.
    Note, this function will not create periodic curves, but it will
    create closed curves.
    Parameters:
      surface_id = identifier of the surface to create the curve on
      points = list of 3D points that lie on the specified surface.
               The list must contain at least 2 points
    Returns:
      id of the new curve object if successful
      None on error
    """
    surface_id = rhutil.coerceguid(surface_id)
    if( surface_id==None ): return scriptcontext.errorhandler()
    objref = Rhino.DocObjects.ObjRef(surface_id)
    points = rhutil.coerce3dpointlist(points)
    surface = objref.Surface()
    if( points==None or surface==None ): return scriptcontext.errorhandler()
    tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    curve = surface.InterpolatedCurveOnSurface(points, tolerance)
    if( curve==None ): return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddCurve(curve)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddInterpCrvOnSrfUV( surface_id, points ):
    """
    Adds an interpolated curve object based on surface parameters, that
    lies on a specified surface. Note, this function will not create
    periodic curves, but it will create closed curves.
    Parameters:
      surface_id = identifier of the surface to create the curve on
      points = list of 2D surface parameters. The list must contain
               at least 2 sets of parameters
    Returns:
      id of the new curve object if successful
      None on error
    """
    surface_id = rhutil.coerceguid(surface_id)
    if( surface_id==None ): return scriptcontext.errorhandler()
    objref = Rhino.DocObjects.ObjRef(surface_id)
    points = rhutil.coerce2dpointlist(points)
    surface = objref.Surface()
    if( points==None or surface==None ): return scriptcontext.errorhandler()
    tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    curve = surface.InterpolatedCurveOnSurfaceUV(points, tolerance)
    if( curve==None ): return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddCurve(curve)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddInterpCurve( points, degree=3, knotstyle=0, start_tangent=None, end_tangent=None ):
    """
    Adds an interpolated curve object to the document. Options exist to make a
    periodic curve or to specify the tangent at the endpoints. The resulting
    curve is a non-rational NURBS curve of the specified degree.
    Parameters:
      points = list containing 3D points to interpolate. For periodic curves,
          if the final point is a duplicate of the initial point, it is
          ignored. The number of control points must be >= (degree+1).
      degree[opt] = The degree of the curve (must be >=1).
          Periodic curves must have a degree >= 2. For knotstyle = 1 or 2,
          the degree must be 3. For knotstyle = 4 or 5, the degree must be odd
      knotstyle[opt]
          0 Uniform knots.  Parameter spacing between consecutive knots is 1.0.
          1 Chord length spacing.  Requires degree = 3 with arrCV1 and arrCVn1 specified.
          2 Sqrt (chord length).  Requires degree = 3 with arrCV1 and arrCVn1 specified.
          3 Periodic with uniform spacing.
          4 Periodic with chord length spacing.  Requires an odd degree value.
          5 Periodic with sqrt (chord length) spacing.  Requires an odd degree value.
      start_tangent [opt] = 3d vector that specifies a tangency condition at the
          beginning of the curve. If the curve is periodic, this argument must be omitted.
      end_tangent [opt] = 3d vector that specifies a tangency condition at the
          end of the curve. If the curve is periodic, this argument must be omitted.
    Returns:
      id of the new curve object if successful
      None on error
    """
    points = rhutil.coerce3dpointlist(points)
    if( points == None ): return scriptcontext.errorhandler()
    start_tangent = rhutil.coerce3dvector(start_tangent)
    if( start_tangent==None ): start_tangent = Rhino.Geometry.Vector3d.Unset
    end_tangent = rhutil.coerce3dvector(end_tangent)
    if( end_tangent==None ): end_tangent = Rhino.Geometry.Vector3d.Unset
    curve = Rhino.Geometry.Curve.CreateInterpolatedCurve(points, degree, knotstyle, start_tangent, end_tangent)
    if( curve == None ): return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddCurve(curve)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddLine( start, end ):
    """
    Adds a line curve to the current model.
    Parameters:
      start, end = end points of the line
    Returns:
      id of the new curve object if successful
      None on error
    """
    start = rhutil.coerce3dpoint(start)
    end = rhutil.coerce3dpoint(end)
    if( start==None or end==None ): return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddLine(start, end)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddNurbsCurve( points, knots, degree, weights=None ):
    """
    Adds a NURBS curve object to the document
    Parameters:
      points = list containing 3D control points
      knots = Knot values for the curve. The number of elements in knots must
          equal the number of elements in points plus degree minus 1
      degree = degree of the curve. must be greater than of equal to 1
      weights[opt] = weight values for the curve. Number of elements should
          equal the number of elements in points. Values must be greater than 0
    """
    points = rhutil.coerce3dpointlist(points)
    if( points==None ): return scriptcontext.errorhandler()
    cvcount = len(points)
    knotcount = cvcount + degree - 1
    if( len(knots) != knotcount ): return scriptcontext.errorhandler()
    if( weights!=None and len(weights)!=cvcount ): return scriptcontext.errorhandler()
    rational = (weights!=None)
    
    nc = Rhino.Geometry.NurbsCurve(3,rational,degree+1,cvcount)
    for i in xrange(cvcount):
        cp = Rhino.Geometry.ControlPoint()
        cp.Location = points[i]
        if weights: cp.Weight = weights[i]
        nc.Points[i] = cp
    for i in xrange(knotcount): nc.Knots[i] = knots[i]
    rc = scriptcontext.doc.Objects.AddCurve(nc)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddPolyline( points ):
    """
    Adds a polyline curve to the current model
    Parameters:
      points = list of 3D points. Duplicate, consecutive points found in
               the array will be removed. The array must contain at least
               two points. If the array contains less than four points,
               then the first point and the last point must be different.
    Returns:
      id of the new curve object if successful
      None on error
    """
    points = rhutil.coerce3dpointlist(points)
    if( points==None ): return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddPolyline(points)
    if( rc==System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def AddSubCrv( curve_id, param0, param1 ):
    """
    Adds a curve object based on a portion, or interval of an existing curve
    object. Similar in operation to Rhino's SubCrv command
    Parameters:
      curve_id = identifier of a closed planar curve object
      param0, param1 = first and second parameters on the source curve
    Returns:
      id of the new curve object if successful
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if( curve == None ): return scriptcontext.errorhandler()
    trimcurve = curve.Trim(param0, param1)
    if( trimcurve == None ): return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddCurve(trimcurve)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc

def ArcAngle( curve_id, segment_index=-1 ):
    """
    Returns the angle of an arc curve object.
    Parameters:
      curve_id = identifier of a curve object
      segment_index [opt] = identifies the curve segment if 
      curve_id identifies a polycurve
    Returns:
      The angle in degrees if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve == None ): return scriptcontext.errorhandler()
    rc, arc = curve.TryGetArc( Rhino.RhinoMath.ZeroTolerance )
    if not rc: return scriptcontext.errorhandler()
    return arc.AngleDegrees


def ArcCenterPoint( curve_id, segment_index=-1 ):
    """
    Returns the center point of an arc curve object
    Parameters:
      curve_id = identifier of a curve object
      segment_index [opt] = identifies the curve segment if
      curve_id identifies a polycurve
    Returns:
      The 3D center point of the arc if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve == None ): return scriptcontext.errorhandler()
    rc, arc = curve.TryGetArc( Rhino.RhinoMath.ZeroTolerance )
    if not rc: return scriptcontext.errorhandler()
    return arc.Center


def ArcMidPoint( curve_id, segment_index=-1 ):
    """
    Returns the mid point of an arc curve object
    Parameters:
      curve_id = identifier of a curve object
      segment_index [opt] = identifies the curve segment if
      curve_id identifies a polycurve
    Returns:
      The 3D mid point of the arc if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve == None ): return scriptcontext.errorhandler()
    rc, arc = curve.TryGetArc( Rhino.RhinoMath.ZeroTolerance )
    if not rc: return scriptcontext.errorhandler()
    return arc.MidPoint


def ArcRadius( curve_id, segment_index=-1 ):
    """
    Returns the radius of an arc curve object
    Parameters:
      curve_id = identifier of a curve object
      segment_index [opt] = identifies the curve segment if 
      curve_id identifies a polycurve
    Returns:
      The radius of the arc if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve == None ): return scriptcontext.errorhandler()
    rc, arc = curve.TryGetArc( Rhino.RhinoMath.ZeroTolerance )
    if not rc: return scriptcontext.errorhandler()
    return arc.Radius


def CircleCenterPoint( curve_id, segment_index=-1 ):
    """
    Returns the center point of a circle curve object
    Parameters:
      curve_id = identifier of a curve object
      segment_index [opt] = identifies the curve segment if
      curve_id identifies a polycurve
    Returns:
      The 3D center point of the circle if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve == None ): return scriptcontext.errorhandler()
    rc, circle = curve.TryGetCircle( Rhino.RhinoMath.ZeroTolerance )
    if not rc: return scriptcontext.errorhandler()
    return circle.Center

def CircleCircumference( curve_id, segment_index=-1 ):
    """
    Returns the circumference of a circle curve object
    Parameters:
      curve_id = identifier of a curve object
      segment_index [opt] = identifies the curve segment if
      curve_id identifies a polycurve
    Returns:
      The circumference of the circle if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve == None ): return scriptcontext.errorhandler()
    rc, circle = curve.TryGetCircle( Rhino.RhinoMath.ZeroTolerance )
    if not rc: return scriptcontext.errorhandler()
    return circle.Circumference

def CircleRadius( curve_id, segment_index=-1 ):
    """
    Returns the radius of a circle curve object
    Parameters:
      curve_id = identifier of a curve object
      segment_index [opt] = identifies the curve segment if
      curve_id identifies a polycurve
    Returns:
      The radius of the circle if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve == None ): return scriptcontext.errorhandler()
    rc, circle = curve.TryGetCircle( Rhino.RhinoMath.ZeroTolerance )
    if not rc: return scriptcontext.errorhandler()
    return circle.Radius

def CloseCurve( curve_id, tolerance=-1.0 ):
    """
    Closes an open curve object by making adjustments to the end points so
    they meet at a point
    Parameters:
      curve_id = identifier of a curve object
      tolerance[opt] = maximum allowable distance between start and end
          point. If omitted, the current absolute tolerance is used
    Returns:
      id of the new curve object if successful
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if( curve==None or curve.IsClosed ): return scriptcontext.errorhandler()
    if( tolerance < 0.0 ): tolerance = Rhino.RhinoMath.ZeroTolerance
    if( curve.MakeClosed(tolerance) != True ): return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddCurve(curve)
    if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc

def ClosedCurveOrientation( curve_id, direction=[0,0,1] ):
    """
    Determine the orientation (counter-clockwise or clockwise) of a closed,
    planar curve
    Parameters:
      curve_id = identifier of a curve object
      direction[opt] = 3d vector that identifies up, or Z axs, direction of
          the plane to test against
    Returns:
      1 if the curve's orientation is clockwise
      -1 if the curve's orientation is counter-clockwise
      0 if unable to compute the curve's orientation
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    direction = rhutil.coerce3dvector(direction)
    if( curve==None or direction==None or curve.IsClosed==False ):
        return scriptcontext.errorhandler()
    orientation = curve.ClosedCurveOrientation(direction)
    return int(orientation)


def ConvertCurveToPolyline( curve_id, angle_tolerance=5.0, tolerance=0.01, delete_input=False):
    """
    Converts a curve to a polyline curve
    Parameters:
      curve_id = identifier of a curve object
      angle_tolerance [opt] = The maximum angle between curve
                        tangents at line endpoints. If omitted,
                        the angle tolerance is set to 5.0.
      tolerance [opt] = The distance tolerance at segment midpoints.
                        If omitted, the tolerance is set to 0.01.
      delete_input [opt] = Delete the curve object specified by strObject.
                        If omitted, strObject will not be deleted.
    Returns:
      The new curve if successful.
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if(curve == None): return scriptcontext.errorhandler()
    if( angle_tolerance<=0 ): angle_tolerance = 5.0
    angle_tolerance = Rhino.RhinoMath.ToRadians(angle_tolerance)
    if( tolerance <= 0.0 ): tolerance = 0.01;
    polyline_curve = curve.ToPolyline( 0, 0, angle_tolerance, 0.0, 0.0, tolerance, 0.0, 0.0, True)
    if( polyline_curve==None ): return scriptcontext.errorhandler()
    id = System.Guid.Empty
    if delete_input:
        if( scriptcontext.doc.Objects.Replace( curve_id, polyline_curve ) ): id = curve_id
    else:
        id = scriptcontext.doc.Objects.AddCurve( polyline_curve )
    if( System.Guid.Empty == id ): return scriptcontext.errorhandler()
    return id
  
def CurveArcLengthPoint( curve_id, length, from_start):
    """
    Returns the point on the curve that is a specified arc length
    from the start of the curve.
    Parameters:
      curve_id = identifier of a curve object
      length = The arc length from the start of the curve to evaluate.
      from_start[opt] = If not specified or True, then the arc length point is
          calculated from the start of the curve. If False, the arc length
          point is calculated from the end of the curve.
    Returns:
      Point3d if successful, or None on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if(curve == None): return scriptcontext.errorhandler()
    curve_length = curve.GetLength()
    if(curve_length >= length):
        s = 0.0
        if( length == 0.0 ): s = 0.0
        elif( length == curve_length ): s = 1.0
        else: s = length / curve_length
        dupe = curve.Duplicate()
        if dupe:
            if( from_start==False ): dupe.Reverse()
            rc, t = dupe.NormalizedLengthParameter(s)
            if rc: return dupe.PointAt(t)
            dupe.Dispose()


def CurveArea( curve_id ):
    """
    Returns area of closed planar curves. The results are based on the
    current drawing units.
    Parameters:
      curve_id = The identifier of a closed, planar curve object.
    Returns:
      List of area information if successful. The list will contain
      the following information:
        Element  Description
        0        The area. If more than one curve was specified, the
                 value will be the cumulative area.
        1        The absolute (+/-) error bound for the area.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if(curve == None): return scriptcontext.errorhandler()
    mp = Rhino.Geometry.AreaMassProperties.Compute(curve)
    if mp: return mp.Area, mp.AreaError
    return scriptcontext.errorhandler()


def CurveAreaCentroid( curve_id ):
    """
    Returns area centroid of closed, planar curves. The results are based
    on the current drawing units.
    Parameters:
      curve_id = The identifier of a closed, planar curve object.
    Returns:
      Tuple of area centroid information if successful. The list will contain
      the following information:
      
        Element  Description
        0        The 3d centroid point. If more than one curve was specified,
                 the value will be the cumulative area.
        1        A 3d vector with the absolute (+/-) error bound for the area
                 centroid.
   
      None on error.    
    """
    curve = rhutil.coercecurve(curve_id)
    if(curve == None): return scriptcontext.errorhandler()
    mp = Rhino.Geometry.AreaMassProperties.Compute(curve)
    if mp: return mp.Centroid, mp.CentroidError
    return scriptcontext.errorhandler()

def CurveArrows(curve_id, arrow_style=None):
    """
    Enables or disables a curve object's annotation arrows
    Parameters:
      curve_id = identifier of a curve
      arrow_style[opt] = the style of annotation arrow to be displayed
        0 = no arrows
        1 = display arrow at start of curve
        2 = display arrow at end of curve
        3 = display arrow at both start and end of curve
      Returns:
        if arrow_style is not specified, the current annotation arrow style
        if arrow_style is specified, the previos arrow style
        None on error
    """
    id = rhutil.coerceguid(curve_id)
    if( id==None ): return None
    objref = Rhino.DocObjects.ObjRef(id)
    curve = objref.Curve()
    rc = None
    if( curve!=None ):
        attr = objref.Object().Attributes
        rc = attr.ObjectDecoration
        if( arrow_style!=None ):
            if( arrow_style==0 ):
                attr.ObjectDecoration = Rhino.DocObjects.ObjectDecoration.None
            elif( arrow_style==1 ):
                attr.ObjectDecoration = Rhino.DocObjects.ObjectDecoration.StartArrowhead
            elif( arrow_style==2 ):
                attr.ObjectDecoration = Rhino.DocObjects.ObjectDecoration.EndArrowhead
            elif( arrow_style==3 ):
                attr.ObjectDecoration = Rhino.DocObjects.ObjectDecoration.BothArrowhead
            scriptcontext.doc.Objects.ModifyAttributes(objref, attr, True)
            scriptcontext.doc.Views.Redraw()
    objref.Dispose()
    if( rc == Rhino.DocObjects.ObjectDecoration.None ): return 0
    if( rc == Rhino.DocObjects.ObjectDecoration.StartArrowhead ): return 1
    if( rc == Rhino.DocObjects.ObjectDecoration.EndArrowhead ): return 2
    if( rc == Rhino.DocObjects.ObjectDecoration.BothArrowhead ): return 3


def CurveBooleanDifference(curve_id_0, curve_id_1):
    """
    Calculates the difference between two closed, planar curves and
    adds the results to the document. Note, curves must be coplanar.
    Parameters:
      curve_id_0 = identifier of the first curve object.
      curve_id_1 = identifier of the second curve object.
    Returns:
      The identifiers of the new objects if successful, None on error.
    """
    curve0 = rhutil.coercecurve(curve_id_0)
    curve1 = rhutil.coercecurve(curve_id_1)
    if( curve0==None or curve1==None ): return scriptcontext.errorhandler()
    
    out_curves = Rhino.Geometry.Curve.CreateBooleanDifference(curve0, curve1)
    curves = []
    for curve in out_curves:
        if(curve and curve.IsValid):
            rc = scriptcontext.doc.Objects.AddCurve(curve)
            curve.Dispose()
            if( rc==System.Guid.Empty ): return scriptcontext.errorhandler()
            curves.append(rc)
    scriptcontext.doc.Views.Redraw()
    return curves

def CurveBooleanIntersection(curve_id_0, curve_id_1):
    """
    Calculates the intersection of two closed, planar curves and adds
    the results to the document. Note, curves must be coplanar.
    Parameters:
      curve_id_0 = identifier of the first curve object.
      curve_id_1 = identifier of the second curve object.
    Returns:
      The identifiers of the new objects if successful, None on error.
    """
    curve0 = rhutil.coercecurve(curve_id_0)
    curve1 = rhutil.coercecurve(curve_id_1)
    if(curve0==None or curve1==None): return scriptcontext.errorhandler()
    
    out_curves = Rhino.Geometry.Curve.CreateBooleanIntersection(curve0, curve1)
    curves = []
    for curve in out_curves:
        if(curve and curve.IsValid):
            rc = scriptcontext.doc.Objects.AddCurve(curve)
            curve.Dispose()
            if( rc==System.Guid.Empty ): return scriptcontext.errorhandler()
            curves.append(rc)
    scriptcontext.doc.Views.Redraw()
    return curves
  
def CurveBooleanUnion(curve_id):
    """
    Calculates the union of two or more closed, planar curves and
    adds the results to the document. Note, curves must be coplanar.
    Parameters:
      curve_id = list of two or more close planar curves identifiers
    Returns:
      The identifiers of the new objects if successful, None on error.
    """
    in_curves = []
    for id in curve_id:
        curve = rhutil.coercecurve(id)
        if curve: in_curves.append(curve)
    
    if (len(in_curves) < 2): return scriptcontext.errorhandler()
    out_curves = Rhino.Geometry.Curve.CreateBooleanUnion(in_curves)
    curves = []
    for curve in out_curves:
        if (curve and curve.IsValid):
            rc = scriptcontext.doc.Objects.AddCurve(curve)
            curve.Dispose()
            if( rc == System.Guid.Empty ): return scriptcontext.errorhandler()
            curves.append(rc)
    scriptcontext.doc.Views.Redraw()
    return curves


def CurveBrepIntersect(curve_id, brep_id, tolerance=None):
    """
    Intersects a curve object with a brep object. Note, unlike the
    CurveSurfaceIntersection function, this function works on trimmed
    surfaces.
    Parameters:
      curve_id = identifier of a curve object
      brep_id = identifier of a brep object
      tolerance [opt] = The distance tolerance at segment midpoints.
                        If omitted, the current absolute tolerance is used.
    Returns:
      List of identifiers for the newly created intersection curve and
      point objects if successful. None on error.            
    """
    curve = rhutil.coercecurve(curve_id)
    brep = rhutil.coercebrep(brep_id)
    if(curve==None or brep==None): return scriptcontext.errorhandler()
    if(tolerance==None or tolerance<0):
        tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    rc, out_curves, out_points = Rhino.Geometry.Intersect.Intersection.CurveBrep(curve, brep, tolerance)
    if not rc: return scriptcontext.errorhandler()
    
    curves = []
    points = []
    for curve in out_curves:
        if(curve and curve.IsValid):
            rc = scriptcontext.doc.Objects.AddCurve(curve)
            curve.Dispose()
            if( rc==System.Guid.Empty ): return scriptcontext.errorhandler()
            curves.append(rc)
        
    for point in out_points:
        if (point and point.IsValid):
            rc = scriptcontext.doc.Objects.AddPoint(point)
            points.append(rc)
    if points: scriptcontext.doc.Views.Redraw()
    return curves, points


def CurveClosestObject(curve_id, object_ids):
    """
    Returns the 3-D point locations on two objects where they are closest
    to each other. Note, this function provides similar functionality to
    that of Rhino's ClosestPt command.
    Parameters:
      curve_id = identifier of a closed planar curve object
      object_ids = list of identifiers of one or more closed, planar curves
    Returns:
      Tuple containing the results of the closest point calculation if
      successful. The elements are as follows:
        0    The identifier of the closest object.
        1    The 3-D point that is closest to the closest object. 
        2    The 3-D point that is closest to the test curve.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if( curve==None ): return scriptcontext.errorhandler()
    geometry = []
    ids = []
    id = rhutil.coerceguid(object_ids)
    if( id!=None ):
        ids.append(id)
        rhobj = scriptcontext.doc.Objects.Find(id)
        if( rhobj==None ): return scriptcontext.errorhandler()
        geometry.append( rhobj.Geometry )
    else:
        for object_id in object_ids:
            id = rhutil.coerceguid(object_id)
            if( id!=None ):
                rhobj = scriptcontext.doc.Objects.Find(id)
                if( rhobj!=None ):
                    geometry.append( rhobj.Geometry )
                    ids.append(id)
    if not geometry: return scriptcontext.errorhandler()
    success, curve_point, geom_point, which_geom = curve.ClosestPoints(geometry, 0.0)
    if success: return ids[which_geom], geom_point, curve_point

    
def CurveClosestPoint(curve_id, test_point, segment_index=-1 ):
    """
    Returns parameter of the point on a curve that is closest to a test point.
    Parameters:
      curve_id = identifier of a curve object
      point = sampling point
      segment_index [opt] = curve segment if curve_id identifies a polycurve
    Returns:
      The parameter of the closest point on the curve if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if (curve==None): return scriptcontext.errorhandler()
    point = rhutil.coerce3dpoint(test_point)
    rc, t = curve.ClosestPoint(point, 0.0)
    if not rc: return scriptcontext.errorhandler()
    return t


def CurveContourPoints(curve_id, start_point, end_point, interval=None):
    """
    Returns the 3-D point locations calculated by contouring a curve object.
    Parameters:
      curve_id = identifier of a curve object.
      start_point = 3-D starting point of a center line.
      end_point = 3-D ending point of a center line.
      interval [opt] = The distance between contour curves. If omitted, 
      the interval will be equal to the diagonal distance of the object's
      bounding box divided by 50.
    Returns:
      A list of 3-D points, one for each contour, if successful.
      None on error.  
    """
    curve = rhutil.coercecurve(curve_id)
    start_point = rhutil.coerce3dpoint(start_point)
    end_point = rhutil.coerce3dpoint(end_point)
    if (curve==None or start_point==None or end_point==None):
        return scriptcontext.errorhandler()
    if( start_point.DistanceTo(end_point) < Rhino.RhinoMath.ZeroTolerance ):
        return scriptcontext.errorhandler()
    if not interval:
        bbox = curve.GetBoundingBox(True)
        diagonal = bbox.Max - bbox.Min
        interval = diagonal.Length / 50.0
    rc = curve.DivideAsContour( start_point, end_point, interval )
    return list(rc)


def CurveCurvature(curve_id, parameter):
    """
    Returns the curvature of a curve at a parameter. See the Rhino help for
    details on curve curvature
    Parameters:
      curve_id = identifier of the curve
      parameter = parameter to evaluate
    Returns:
      Tuple of curvature information on success
        element 0 = point at specified parameter
        element 1 = tangent vector
        element 2 = center of radius of curvature
        element 3 = radius of curvature
        element 4 = curvature vector
      None on failure
    """
    curve = rhutil.coercecurve(curve_id)
    if(curve == None): return scriptcontext.errorhandler()
    point = curve.PointAt(parameter)
    tangent = curve.TangentAt(parameter)
    if( tangent.IsTiny(0) ): return scriptcontext.errorhandler()
    cv = curve.CurvatureAt(parameter)
    k = cv.Length
    if( k < Rhino.RhinoMath.SqrtEpsilon ): return scriptcontext.errorhandler()
    rv = cv / (k*k)
    circle = Rhino.Geometry.Circle(point, tangent, point + 2.0*rv)
    center = point + rv
    radius = circle.Radius
    return point, tangent, center, radius, cv


def CurveCurveIntersection(curveA, curveB, tolerance=-1):
    """
    Calculates the intersection of two curve objects.
    Parameters:
      curveA = The identifier of the first curve object.
      curveB = The identifier of the second curve object. If omitted, then a
               self-intersection test will be performed on curveA.
      tolerance [opt] = The absolute tolerance in drawing units. If omitted,
                        the document's current absolute tolerance is used.
    Returns:
      A two-dimensional list of intersection information if successful.
      The list will contain one or more of the following elements:
        Element Type     Description
        (n, 0)  Number   The intersection event type, either Point (1) or Overlap (2).
        (n, 1)  Point3d  If the event type is Point (1), then the intersection point 
                         on the first curve. If the event type is Overlap (2), then
                         intersection start point on the first curve.
        (n, 2)  Point3d  If the event type is Point (1), then the intersection point
                         on the first curve. If the event type is Overlap (2), then
                         intersection end point on the first curve.
        (n, 3)  Point3d  If the event type is Point (1), then the intersection point 
                         on the second curve. If the event type is Overlap (2), then
                         intersection start point on the second curve.
        (n, 4)  Point3d  If the event type is Point (1), then the intersection point
                         on the second curve. If the event type is Overlap (2), then
                         intersection end point on the second curve.
        (n, 5)  Number   If the event type is Point (1), then the first curve parameter.
                         If the event type is Overlap (2), then the start value of the
                         first curve parameter range.
        (n, 6)  Number   If the event type is Point (1), then the first curve parameter.
                         If the event type is Overlap (2), then the end value of the
                         first curve parameter range.
        (n, 7)  Number   If the event type is Point (1), then the second curve parameter.
                         If the event type is Overlap (2), then the start value of the
                         second curve parameter range.
        (n, 8)  Number   If the event type is Point (1), then the second curve parameter.
                         If the event type is Overlap (2), then the end value of the 
                         second curve parameter range.
      None of not successful, or on error.
    """
    curveA = rhutil.coercecurve(curveA)
    curveB = rhutil.coercecurve(curveB)
    if(not curveA or not curveB): return scriptcontext.errorhandler()
    if (tolerance==None or tolerance < 0.0):
        tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    rc = Rhino.Geometry.Intersect.Intersection.CurveCurve(curveA, curveB, tolerance, 0.0)
    if not rc: return scriptcontext.errorhandler()
    events = []
    for i in xrange(rc.Count):
        event_type = 1
        if( rc[i].IsOverlap ): event_type = 2
        oa = rc[i].OverlapA
        ob = rc[i].OverlapB
        element = (event_type, rc[i].PointA, rc[i].PointA2, rc[i].PointB, rc[i].PointB2, oa[0], oa[1], ob[0], ob[1])
        events.append(element)
    if events: return events
    return scriptcontext.errorhandler()


def CurveDegree(curve_id, segment_index=-1):
    """
    Returns the degree of a curve object.
    Parameters:
      curve_id = identifier of a curve object.
      segment_index [opt] = the curve segment if curve_id identifies a polycurve.
    Returns:
      The degree of the curve if successful. None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if (curve == None): return scriptcontext.errorhandler()
    return curve.Degree


def CurveDeviation( curve_a, curve_b ):
    """
    Returns the minimum and maximum deviation between two curve objects
    Parameters:
      curve_a, curve_b = identifiers of two curves
    Returns:
      tuple of deviation information on success
        element 0 = curve_a parameter at maximum overlap distance point
        element 1 = curve_b parameter at maximum overlap distance point
        element 2 = maximum overlap distance
        element 3 = curve_a parameter at minimum overlap distance point
        element 4 = curve_b parameter at minimum overlap distance point
        element 5 = minimum distance between curves
      None on error
    """
    curve_a = rhutil.coercecurve( curve_a )
    curve_b = rhutil.coercecurve( curve_b )
    if( curve_a==None or curve_b==None ): return scriptcontext.errorhandler()
    tol = scriptcontext.doc.ModelAbsoluteTolerance
    rc = Rhino.Geometry.Curve.GetDistancesBetweenCurves(curve_a, curve_b, tol)
    if not rc[0]: return scriptcontext.errorhandler()
    maxa = rc[2]
    maxb = rc[3]
    maxd = rc[1]
    mina = rc[5]
    minb = rc[6]
    mind = rc[4]
    return maxa, maxb, maxd, mina, minb, mind


def CurveDim(curve_id, segment_index=-1):
    """
    Returns the dimension of a curve object
    Parameters:
      curve_id = identifier of a curve object.
      segment_index [opt] = the curve segment if curve_id identifies a polycurve.
    Returns:
      The dimension of the curve if successful. None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if (curve == None): return scriptcontext.errorhandler()
    return curve.Dimension


def CurveDirectionsMatch(curve_id_0, curve_id_1):
    """
    Tests if two curve objects are generally in the same direction
    or if they would be more in the same direction if one of them
    were flipped. When testing curve directions, both curves must
    be either open or closed - you cannot test one open curve and
    one closed curve.
    Parameters:
      curve_id_0 = identifier of first curve object
      curve_id_1 = identifier of second curve object
    Returns:
      True if the curve directions match, otherwise False. 
      None on error.
    """
    curve0 = rhutil.coercecurve(curve_id_0)
    curve1 = rhutil.coercecurve(curve_id_1)
    if(curve0 == None or curve1 == None): return scriptcontext.errorhandler()
    return Rhino.Geometry.Curve.DoDirectionsMatch(curve0, curve1)


def CurveDiscontinuity(curve_id, style):   
    """
    Search for a derivatitive, tangent, or curvature discontinuity in
    a curve object.
    Parameters:
      curve_id = identifier of curve object
      style = The type of continuity to test for. The types of
          continuity are as follows:
          Value    Description
          1        C0 - Continuous function
          2        C1 - Continuous first derivative
          3        C2 - Continuous first and second derivative
          4        G1 - Continuous unit tangent
          5        G2 - Continuous unit tangent and curvature
    Returns:
      List 3-D points where the curve is discontinuous if successful.
      None on error.   
    """
    curve = rhutil.coercecurve(curve_id)
    if (curve == None): return scriptcontext.errorhandler()
    
    dom = curve.Domain
    t0 = dom.Min
    t1 = dom.Max
    points = []
    get_next = True
    while get_next:
        get_next, t = curve.GetNextDiscontinuity(System.Enum.ToObject(Rhino.Geometry.Continuity, style), t0, t1)
        if get_next:
            points.append(curve.PointAt(t))
            t0 = t # Advance to the next parameter
    return points


def CurveDomain(curve_id, segment_index=-1):
    """
    Returns the domain of a curve object.
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve.
    Returns:
      The domain of the curve if successful. None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if (curve == None): return scriptcontext.errorhandler()
    dom = curve.Domain
    if (dom == None): return scriptcontext.errorhandler()
    return dom.Min, dom.Max


def CurveEditPoints(curve_id, return_parameters=False, segment_index=-1):
    """
    Returns the edit, or Greville, points of a curve object. 
    For each curve control point, there is a corresponding edit point.
    Parameters:
      curve_id = identifier of the curve object
      return_parameters[opt] = if True, return as a list of curve parameters.
        If False, return as a list of 3d points
      segment_index[opt] = the curve segment is curve_id identifies a polycurve
    Returns:
      a list of curve parameters of 3d points on success
      None on error
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve==None ): return scriptcontext.errorhandler()
    nc = curve.ToNurbsCurve()
    if( nc==None ): return scriptcontext.errorhandler()
    if return_parameters: return nc.GrevilleParameters()
    return nc.GrevillePoints()


def CurveEndPoint(curve_id, segment_index=-1):
    """
    Returns the end point of a curve object
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      The 3-D end point of the curve if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if( curve == None ): return scriptcontext.errorhandler()
    return curve.PointAtEnd


def CurveFilletPoints(curve_id_0, curve_id_1, radius=1.0, base_point_0=None, base_point_1=None, return_points=True):
    """
    Find points at which to cut a pair of curves so that a fillet of a
    specified radius fits. A fillet point is a pair of points
    (point0, point1) such that there is a circle of radius
    tangent to curve curve0 at point0 and tangent
    to curve curve1 at point1. Of all possible fillet points,
    this function returns the one which is the closest to the base
    point base_point_0, base_point_1. Distance from the base point
    is measured by  the sum of arc lengths along the two curves. 
    Parameters:
      curve_id_0 = identifier of the first curve object.
      curve_id_1 = identifier of the second curve object.
      radius [opt] = The fillet radius. If omitted, a radius
                     of 1.0 is specified.
      base_point_0 [opt] = The base point on the first curve.
                     If omitted, the starting point of the curve is used.
      base_point_1 [opt] = The base point on the second curve. If omitted,
                     the starting point of the curve is used.
      return_points [opt] = If True (Default), then fillet points are
                     returned. Otherwise, a fillet curve is created and
                     it's identifier is returned.
    Returns:
      If return_points is True, then a list of point and vector values
      if successful. The list elements are as follows:
      
      0    A point on the first curve at which to cut (arrPoint0).
      1    A point on the second curve at which to cut (arrPoint1).
      2    The fillet plane's origin (3-D point). This point is also
           the center point of the fillet
      3    The fillet plane's X axis (3-D vector).
      4    The fillet plane's Y axis (3-D vector).
      5    The fillet plane's Z axis (3-D vector).
      
      If return_points is False, then the identifier of the fillet curve
      if successful.
      None if not successful, or on error.                  
    """
    curve0 = rhutil.coercecurve(curve_id_0)
    curve1 = rhutil.coercecurve(curve_id_1)
    if( curve0==None or curve1==None ): return scriptcontext.errorhandler()
    t0_base = curve0.Domain.Min
    
    if base_point_0:
        rc = curve0.ClosestPoint(base_point_0, t0_base)
        if (rc[0] != True): return scriptcontext.errorhandler()
    
    t1_base = curve1.Domain.Min
    if base_point_1:
        rc = curve1.ClosestPoint(base_point_1, t1_base)
        if (rc[0] != True): return scriptcontext.errorhandler()

    r = radius if (radius and radius>0) else 1.0
    rc = Rhino.Geometry.Curve.GetFilletPoints(curve0, curve1, r, t0_base, t1_base)
    if (rc[0] != False):
        point_0 = curve0.PointAt( rc[1] )
        point_1 = curve1.PointAt( rc[2] )
        return [point_0, point_1, rc[3].Origin, rc[3].XAxis, rc[3].YAxis, rc[3].ZAxis]
    return scriptcontext.errorhandler()


def CurveFrame(curve_id, parameter, segment_index=-1 ):
    """
    Returns the plane at a parameter of a curve. The plane is based on the
    tangent and curvature vectors at a parameter.
    Parameters:
      curve_id = identifier of the curve object.
      parameter = parameter to evaluate.
      segment_index [opt] = 
    Returns:
      The plane at the specified parameter if successful. 
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    if curve.Domain.IncludesParameter(parameter):
        rc, frame = curve.FrameAt(parameter)
        if rc and frame.IsValid: return frame
    return scriptcontext.errorhandler()


def CurveKnotCount(curve_id, segment_index=-1):
    """
    Returns the knot count of a curve object.
    Parameters:
      curve_id = identifier of the curve object.
      segment_index [opt] = the curve segment if curve_id identifies a polycurve.
    Returns:
      The number of knots if successful.
      None if not successful or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    nc = curve.ToNurbsCurve()
    if nc is None: return scriptcontext.errorhandler()
    return nc.Knots.Count


def CurveKnots(curve_id, segment_index=-1):
    """
    Returns the knots, or knot vector, of a curve object
    Parameters:
      curve_id = identifier of the curve object.
      segment_index [opt] = the curve segment if curve_id identifies a polycurve.
    Returns:
      knot values if successful.
      None if not successful or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    nc = curve.ToNurbsCurve()
    if nc is None: return scriptcontext.errorhandler()
    return nc.Knots

def CurveLength(curve_id, segment_index=-1, sub_domain=None):
    """
    Returns the length of a curve object.
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
      sub_domain [opt] = list of two numbers identifing the sub-domain of the
          curve on which the calculation will be performed. The two parameters
          (sub-domain) must be non-decreasing. If omitted, the length of the
          entire curve is returned.
    Returns:
      The length of the curve if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    if sub_domain:
        if(len(sub_domain) == 2):
            dom = Rhino.Geometry.Interval(sub_domain[0], sub_domain[1])
            return curve.GetLength(dom)
        return scriptcontext.errorhandler()
    return curve.GetLength()


def CurveMidPoint(curve_id, segment_index=-1):
    """
    Returns the mid point of a curve object.
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      The 3-D mid point of the curve if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    rc, t = curve.NormalizedLengthParameter(0.5)
    if rc: return curve.PointAt(t)
    return scriptcontext.errorhandler()


def CurveNormal(curve_id, segment_index=-1):
    """
    Returns the normal direction of the plane in which a planar curve object lies.
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      The 3-D normal vector if sucessful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    tol = scriptcontext.doc.ModelAbsoluteTolerance
    rc, plane = curve.TryGetPlane(tol)
    if rc: return plane.Normal
    return scriptcontext.errorhandler()


def CurveNormalizedParameter(curve_id, parameter):
    """
    Converts a curve parameter to a normalized curve parameter;
    one that ranges between 0-1
    Parameters:
      curve_id = identifier of the curve object
      parameter = the curve parameter to convert
    Returns:
      normalized curve parameter if successful
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    return curve.Domain.NormalizedParameterAt(parameter)


def CurveParameter(curve_id, parameter):
    """
    Converts a normalized curve parameter to a curve parameter;
    one within the curve's domain
    Parameters:
      curve_id = identifier of the curve object
      parameter = the normalized curve parameter to convert
    Returns:
      curve parameter if successful
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    return curve.Domain.ParameterAt(parameter)


def CurvePerpFrame(curve_id, parameter):
    """
    Returns the perpendicular plane at a parameter of a curve. The result
    is relatively parallel (zero-twisting) plane
    Parameters:
        curve_id = identifier of the curve object
        parameter = parameter to evaluate
    Returns:
        Plane on success
        None on error
    """
    curve = rhutil.coercecurve(curve_id)
    parameter = float(parameter)
    if curve is None: return scriptcontext.errorhandler()
    params = (parameter, parameter+0.05)
    if( parameter>0.9 ): params = (parameter-0.05, parameter)
    planes = curve.GetPerpendicularFrames(params)
    if( planes is None or len(planes)<2 ): return scriptcontext.errorhandler()
    if( parameter>0.9 ): return planes[1]
    return planes[0]


def CurvePlane(curve_id, segment_index=-1):
    """
    Returns the plane in which a planar curve lies. Note, this function works
    only on planar curves.
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      The plane in which the curve lies if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    tol = scriptcontext.doc.ModelAbsoluteTolerance
    rc, plane = curve.TryGetPlane(tol)
    if rc: return plane
    return scriptcontext.errorhandler()


def CurvePointCount(curve_id, segment_index=-1):
    """
    Returns the control points count of a curve object.
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      Number of control points if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    nc = curve.ToNurbsCurve()
    if nc: return nc.Points.Count
    return scriptcontext.errorhandler()

def CurvePoints( curve_id, segment_index=-1 ):
    """
    Returns the control points, or control vertices, of a curve object.
    If the curve is a rational NURBS curve, the euclidean control vertices
    are returned.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    nc = curve.ToNurbsCurve()
    if nc is None: return scriptcontext.errorhandler()
    points = []
    for i in xrange(nc.Points.Count):
        points.append(nc.Points[i].Location)
    return points


def CurveRadius(curve_id, test_point, segment_index=-1):
    """
    Returns the radius of curvature at a point on a curve.
    Parameters:
      curve_id = identifier of the curve object
      test_point = sampling point
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      The radius of curvature at the point on the curve if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    point = rhutil.coerce3dpoint(test_point)
    if curve is None or point is None: return scriptcontext.errorhandler()
    rc, t = curve.ClosestPoint(point, 0.0)
    if not rc: return scriptcontext.errorhandler()
    v = curve.CurvatureAt( t )
    k = v.Length()
    if k>Rhino.RhinoMath.ZeroTolerance: return 1/k
    return scriptcontext.errorhandler()


def CurveSeam(curve_id, parameter):
    """
    Adjusts the seam, or start/end, point of a closed curve.
    Parameters:
      curve_id = identifier of the curve object
      parameter = The parameter of the new start/end point. 
                  Note, if successful, the resulting curve's
                  domain will start at dblParameter.
    Returns:
      True or False indicating success or failure.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if (curve is None or not curve.IsClosed or not curve.Domain.IncludesParameter(parameter)):
        return scriptcontext.errorhandler()
    dupe = curve.Duplicate()
    if dupe:
        dupe.ChangeClosedCurveSeam(parameter)
        objref = Rhino.DocObjects.ObjRef(curve_id)
        dupe_obj = scriptcontext.doc.Objects.Replace(objref, dupe)
        return dupe_obj is not None
    return False


def CurveStartPoint(curve_id, segment_index=-1):
    """
    Returns the start point of a curve object
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      The 3-D starting point of the curve if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    return curve.PointAtStart


def CurveSurfaceIntersection(curve_id, surface_id, tolerance=-1, angle_tolerance=-1):
    """
    Calculates the intersection of a curve object with a surface object. Note,
    this function works on the untrimmed portion of the surface.
    Parameters:
      curve_id = The identifier of the first curve object.
      surface_id = The identifier of the second curve object. If omitted,
          the a self-intersection test will be performed on curve.
      tolerance [opt] = The absolute tolerance in drawing units. If omitted, 
          the document's current absolute tolerance is used.
      angle_tolerance [opt] = The angle tolerance in degrees. The angle
          tolerance is used to determine when the curve is tangent to the
          surface. If omitted, the document's current angle tolerance is used.
    Returns:
      A two-dimensional list of intersection information if successful.
      The list will contain one or more of the following elements:
        Element Type     Description
        (n, 0)  Number   The intersection event type, either Point(1) or Overlap(2).
        (n, 1)  Point3d  If the event type is Point(1), then the intersection point 
                         on the first curve. If the event type is Overlap(2), then
                         intersection start point on the first curve.
        (n, 2)  Point3d  If the event type is Point(1), then the intersection point
                         on the first curve. If the event type is Overlap(2), then
                         intersection end point on the first curve.
        (n, 3)  Point3d  If the event type is Point(1), then the intersection point 
                         on the second curve. If the event type is Overlap(2), then
                         intersection start point on the surface.
        (n, 4)  Point3d  If the event type is Point(1), then the intersection point
                         on the second curve. If the event type is Overlap(2), then
                         intersection end point on the surface.
        (n, 5)  Number   If the event type is Point(1), then the first curve parameter.
                         If the event type is Overlap(2), then the start value of the
                         first curve parameter range.
        (n, 6)  Number   If the event type is Point(1), then the first curve parameter.
                         If the event type is Overlap(2), then the end value of the
                         curve parameter range.
        (n, 7)  Number   If the event type is Point(1), then the U surface parameter.
                         If the event type is Overlap(2), then the U surface parameter
                         for curve at (n, 5).
        (n, 8)  Number   If the event type is Point(1), then the V surface parameter.
                         If the event type is Overlap(2), then the V surface parameter
                         for curve at (n, 5).
        (n, 9)  Number   If the event type is Point(1), then the U surface parameter.
                         If the event type is Overlap(2), then the U surface parameter
                         for curve at (n, 6).
        (n, 10) Number   If the event type is Point(1), then the V surface parameter.
                         If the event type is Overlap(2), then the V surface parameter
                         for curve at (n, 6).
      None of not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    surface = rhutil.coercesurface(surface_id)
    if curve is None or surface is None: return scriptcontext.errorhandler()
    if tolerance is None or tolerance<0:
        tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    if angle_tolerance is None or angle_tolerance<0:
        angle_tolerance = scriptcontext.doc.ModelAngleToleranceDegrees
    rc = Rhino.Geometry.Intersect.Intersection.CurveSurface(curve, surface, tolerance, angle_tolerance)
    if rc is None: return scriptcontext.errorhandler()
    events = []
    for i in xrange(rc.Count):
        event_type = 2 if rc[i].IsOverlap else 1
        item = rc[i]
        oa = item.OverlapA
        u,v = item.SurfaceOverlapParameter()
        e = (event_type, item.PointA, item.PointA2, item.PointB, item.PointB2, oa[0], oa[1], u[0], u[1], v[0], v[1])
        events.append(e)
    if events: return events
    return scriptcontext.errorhandler()


def CurveTangent(curve_id, parameter, segment_index=-1):
    """
    Returns a 3-D vector that is the tangent to a curve at a parameter.
    Parameters:
      curve_id = identifier of the curve object
      parameter = parameter to evaluate
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      A 3-D vector if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    rc = Rhino.Geometry.Point3d.Unset
    if curve.Domain.IncludesParameter(parameter):
        return curve.TangentAt(parameter)
    return scriptcontext.errorhandler()


def CurveWeights(curve_id, segment_index=-1):
    """
    Returns list of weights that are assigned to the control points of a curve
    Parameters:
      curve_id = identifier of the curve object
      segment_index[opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      The weight values of the curve if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    nc = curve.NurbsCurve(Rhino.RhinoMath.ZeroTolerance)
    if nc is None: return scriptcontext.errorhandler()
    weights = [nc.Weight(i) for i in xrange(nc.CVCount)]
    return weights


def DivideCurve(curve_id, segments, create_points=False, return_points=True):
    """
    Divides a curve object into a specified number of segments.
    Parameters:
      curve_id = identifier of the curve object
      segments = The number of segments.
      create_points [opt] = Create the division points. If omitted or False,
          points are not created.
      return_points [opt] = If omitted or True, points are returned.
          If False, then a list of curve parameters are returned.
    Returns:
      If return_points is not specified or True, then a list containing 3D
      division points.
      If return_points is False, then an array containing division curve
      parameters.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    rc = curve.DivideByCount(segments, True)
    if not rc: return scriptcontext.errorhandler()
    if return_points or create_points:
        outputpoints = [curve.PointAt(t) for t in rc]
        if return_points: rc = outputpoints
        if create_points:
            for point in outpoints:
                if point.IsValid: scriptcontext.doc.Objects.AddPoint(point)
    return rc


def DivideCurveEquidistant(curve_id, distance, create_points=False, return_points=True):
    """
    Divides a curve such that the linear distance between the points is equal.
    Parameters:
      curve_id = the object's identifier
      distance = linear distance between division points
      create_points [opt] = create the division points
      return_points [opt] = if True, return a list of points. If False, return a list of curve parameters
    Returns:
      A list of points or curve parameters based on the value of return_points
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    points = curve.DivideEquidistant(distance)
    if not points: return scriptcontext.errorhandler()
    if( create_points ):
        [scriptcontext.doc.Objects.AddPoint(point) for point in points]
        scriptcontext.doc.Views.Redraw()
    if( return_points ): return points
    tvals = []
    for point in points:
        rc, t = curve.ClosestPoint(point)
        tvals.append(t)
    return tvals


def DivideCurveLength(curve_id, length, create_points=False, return_points=True):
    """
    Divides a curve object into segments of a specified length.
    Parameters:
      curve_id = identifier of the curve object
      length = The length of each segment.
      create_points [opt] = Create the division points. If omitted or False,
          points are not created.
      return_points [opt] = If omitted or True, points are returned.
          If False, then a list of curve parameters are returned.
    Returns:
      If return_points is not specified or True, then a list containing 3D
      division points if successful.
      If return_points is False, then an array containing division curve
      parameters if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    rc = curve.DivideByLength(length, True)
    if not rc: return scriptcontext.errorhandler()
    if return_points or create_points:
        outputpoints = [curve.PointAt(t) for t in rc]
        if create_points:
            for point in outpoints:
                if (point.IsValid): scriptcontext.doc.Objects.AddPoint(point)
        if return_points: rc = outputpoints
    return rc


def EllipseCenterPoint(curve_id):
    """
    Returns the center point of an elliptical-shaped curve object.
    Parameters:
      curve_id = identifier of the curve object.    
    Returns:
      The 3-D center point of the ellipse if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    rc, ellipse = curve.TryGetEllipse()
    if not rc: return scriptcontext.errorhandler()
    return ellipse.Plane.Origin


def EllipseQuadPoints(curve_id):
    """
    Returns the quadrant points of an elliptical-shaped curve object.
    Parameters:
      curve_id = identifier of the curve object.
    Returns:
      A tuple 3D points identifying the quadrants of the ellipse
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    rc, ellipse = curve.TryGetEllipse()
    if not rc: return scriptcontext.errorhandler()
    
    origin = ellipse.Plane.Origin;
    xaxis = ellipse.Radius1 * ellipse.Plane.XAxis;
    yaxis = ellipse.Radius2 * ellipse.Plane.YAxis;
    return (origin-xaxis, origin+xaxis, origin-yaxis, origin+yaxis)
  
def EvaluateCurve(curve_id, t, segment_index=-1):
    """
    Evaluates a curve at a parameter.
    Parameters:
      curve_id = identifier of the curve object
      t = the parameter to evaluate
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      A 3d point if successful.
      None on error.
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    return curve.PointAt(t)


def ExplodeCurves(curve_ids, delete_input=False):
    """
    Explodes, or un-joins, one more curve objects. Polycurves will be
    exploded into curve segments. Polylines will be exploded into line
    segments. ExplodeCurves will return the curves in topological order. 
    Parameters:
      curve_ids = identifier of the curve object(s) to explode.
      delete_input [opt] = Delete input objects after exploding.
    Returns:
      A list of strings identifying the newly created curve objects
      None on error.
    """
    if( type(curve_ids) is list or type(curve_ids) is tuple ): pass
    else: curve_ids = [curve_ids]
    rc = []
    for id in curve_ids:
        curve = rhutil.coercecurve(id)
        if curve:
            pieces = curve.DuplicateSegments()
            if pieces:
                for piece in pieces:
                    rc.append(scriptcontext.doc.Objects.AddCurve(piece))
                if delete_input:
                    id = rhutil.coerceguid(id)
                    scriptcontext.doc.Objects.Delete(id, True)
    if not rc: return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def ExtendCurve(curve_id, extension_type, side, boundary_object_ids):
    """
    Extends a non-closed curve object by a line, arc, or smooth extension
    until it intersects a collection of objects.
    Parameters:
      curve_id: identifier of curve to extend
      extension_type: 0 = line, 1 = arc, 2 = smooth
      side: 0=extend from the start of the curve, 1=extend from the end of the curve
      boundary_object_ids: curve, surfacem and polysurface objects to extend to
    Returns:
      The identifier of the new object if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    boundary_object_ids = rhutil.coerceguidlist(boundary_object_ids)
    if curve is None or boundary_object_id is None: return scriptcontext.errorhandler()
    if( extension_type==0 ): extension_type = Rhino.Geometry.CurveExtensionStyle.Line
    elif( extension_type==1 ): extension_type = Rhino.Geometry.CurveExtensionStyle.Arc
    elif( extension_type==2 ): extension_type = Rhino.Geometry.CurveExtensionStyle.Smooth
    else: return scriptcontext.errorhandler()
    
    if( side==0 ): side = Rhino.Geometry.CurveEnd.Start
    elif( side==1 ): side = Rhino.Geometry.CurveEnd.End
    elif( side==2 ): side = Rhino.Geometry.CurveEnd.Both
    else: return scriptcontext.errorhandler()
    
    geometry = []
    for id in boundary_object_ids:
        rhobj = scriptcontext.doc.Objects.Find(id)
        if rhobj: geometry.append(rhobj.Geometry)
    if not geometry: return scriptcontext.errorhandler()
    newcurve = curve.Extend(side, extension_type, geometry)
    if( newcurve and newcurve.IsValid ):
        objref = Rhino.DocObjects.ObjRef(curve_id)
        if( scriptcontext.doc.Objects.Replace( objref, newcurve ) ):
            scriptcontext.doc.Views.Redraw()
            return curve_id
    return scriptcontext.errorhandler()


def ExtendCurveLength(curve_id, extension_type, side, length):
    """
    Extends a non-closed curve object by a line, arc, or smooth extension for
    a specified distance
    Parameters:
      curve_id: identifier of curve to extend
      extension_type: 0 = line, 1 = arc, 2 = smooth
      side: 0=extend from start of the curve, 1=extend from end of the curve
      length: distance to extend
    Returns:
      The identifier of the new object
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    if( extension_type==0 ): extension_type = Rhino.Geometry.CurveExtensionStyle.Line
    elif( extension_type==1 ): extension_type = Rhino.Geometry.CurveExtensionStyle.Arc
    elif( extension_type==2 ): extension_type = Rhino.Geometry.CurveExtensionStyle.Smooth
    else: return scriptcontext.errorhandler()
    
    if( side==0 ): side = Rhino.Geometry.CurveEnd.Start
    elif( side==1 ): side = Rhino.Geometry.CurveEnd.End
    elif( side==2 ): side = Rhino.Geometry.CurveEnd.Both
    else: return scriptcontext.errorhandler()
    
    newcurve = curve.Extend(side, length, extension_type)
    if( newcurve and newcurve.IsValid ):
        objref = Rhino.DocObjects.ObjRef(curve_id)
        if( scriptcontext.doc.Objects.Replace( objref, newcurve ) ):
            scriptcontext.doc.Views.Redraw()
            return curve_id
    return scriptcontext.errorhandler()


def ExtendCurvePoint(curve_id, side, point):
    """
    Extends a non-closed curve object by smooth extension to a point
    Parameters:
      curve_id: identifier of curve to extend
      side: 0=extend from start of the curve, 1=extend from end of the curve
      point: point to extend to
    Returns:
      The identifier of the new object if successful.
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    point = rhutil.coerce3dpoint(point)
    if curve is None or point is None: return scriptcontext.errorhandler()
    
    if( side==0 ): side = Rhino.Geometry.CurveEnd.Start
    elif( side==1 ): side = Rhino.Geometry.CurveEnd.End
    elif( side==2 ): side = Rhino.Geometry.CurveEnd.Both
    else: return scriptcontext.errorhandler()
    
    extension_type = Rhino.Geometry.CurveExtensionStyle.Smooth
    newcurve = curve.Extend(side, extension_type, point)
    if( newcurve and newcurve.IsValid ):
        objref = Rhino.DocObjects.ObjRef(curve_id)
        if( scriptcontext.doc.Objects.Replace( objref, newcurve ) ):
            scriptcontext.doc.Views.Redraw()
            return curve_id
    return scriptcontext.errorhandler()


def FairCurve(curve_id, tolerance=1.0):
    """
    Fairs a curve object. Fair works best on degree 3 (cubic) curves. Fair
    attempts to remove large curvature variations while limiting the geometry
    changes to be no more than the specified tolerance. Sometimes several
    applications of this method are necessary to remove nasty curvature problems.
    Parameters:
      curve_id = identifier of the curve object
      tolerance[opt] = fairing tolerance
    Returns:
      True or False indicating success or failure
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    angle_tol = 0.0
    clamp = 0
    if( curve.IsPeriodic ):
        curve = curve.ToNurbsCurve()
        clamp = 1
    newcurve = curve.Fair(tolerance, angle_tol, clamp, clamp, 100)
    if newcurve is None: return scriptcontext.errorhandler()
    curve_id = rhutil.coerceguid(curve_id)
    objref = Rhino.DocObjects.ObjRef(curve_id)
    if( scriptcontext.doc.Objects.Replace(objref, newcurve) ):
        scriptcontext.doc.Views.Redraw()
        return True
    return False


def FitCurve(curve_id, degree=3, distance_tolerance=-1, angle_tolerance=-1):
    """
    Reduces number of curve control points while maintaining the curve's same
    general shape. Use this function for replacing curves with many control
    points. For more information, see the Rhino help for the FitCrv command.
    Parameters:
      curve_id = Identifier of the curve object
      degree [opt] = The curve degree, which must be greater than 1.
                     The default is 3.
      distance_tolerance [opt] = The fitting tolerance. If distance_tolerance
          is not specified or <= 0.0, the document absolute tolerance is used.
      angle_tolerance [opt] = The kink smoothing tolerance in degrees. If
          angle_tolerance is 0.0, all kinks are smoothed. If angle_tolerance
          is > 0.0, kinks smaller than angle_tolerance are smoothed. If
          angle_tolerance is not specified or < 0.0, the document angle
          tolerance is used for the kink smoothing.
    Returns:
      The identifier of the new object
      None if not successful, or on error.
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    if(fit_tolerance is None or fit_tolerance<0):
        fit_tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    if(angle_tolerance is None or angle_tolerance<0):
        angle_tolerance = scriptcontext.doc.ModelAngleToleranceRadians
    nc = curve.Fit(degree, fit_tolerance, angle_tolerance)
    if nc:
        attributes = Rhino.DocObjects.ObjectAttributes(id)
        rc = scriptcontext.doc.Objects.AddCurve(curve, attributes)
        if( rc!=System.Guid.Empty ): return rc
    return scriptcontext.errorhandler()


def InsertCurveKnot( curve_id, parameter, symmetrical=False ):
    """
    Inserts a knot into a curve object
    Parameters:
      curve_id = identifier of the curve object
      parameter = parameter on the curve
      symmetrical[opt] = if True, then knots are added on both sides of
          the center of the curve
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None or not curve.Domain.IncludesParameter(parameter):
        return False
    nc = curve.ToNurbsCurve()
    if not nc: return False
    rc, t = curve.GetNurbsFormParameterFromCurveParameter(parameter)
    if rc:
        rc = nc.Knots.InsertKnot(t,1)
        if rc and symmetrical:
            domain = nc.Domain
            t_sym = domain.T1 - t + domain.T0
            if abs(t_sym)>Rhino.RhinoMath.SqrtEpsilon:
                rc = nc.Knots.InsertKnot(t_sym,1)
        if rc:
            curve_id = rhutil.coerceguid(curve_id)
            objref = Rhino.DocObjects.ObjRef(curve_id)
            rc = scriptcontext.doc.Objects.Replace(objref, nc)
            if rc: scriptcontext.doc.Views.Redraw()
    return rc


def IsArc( curve_id, segment_index=-1 ):
    """
    Verifies an object is an arc curve
    Parameters:
      curve_id = Identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    return curve and curve.IsArc()


def IsCircle( curve_id, segment_index=-1 ):
    """
    Verifies an object is a circle curve
    Parameters:
      curve_id = Identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    return curve and curve.IsCircle()


def IsCurve( object_id ):
    "Verifies an object is a curve"
    curve = rhutil.coercecurve(object_id)
    return curve is not None


def IsCurveClosable( curve_id, tolerance=None ):
    """
    Decide if it makes sense to close off the curve by moving the end point to
    the start point based on start-end gap size and length of curve as
    approximated by chord defined by 6 points
    Parameters:
      curve_id = identifier of the curve object
      tolerance[opt] = maximum allowable distance between start point and end
        point. If omitted, the document's current absolute tolerance is used
    Returns:
      True or False
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    if tolerance is None: tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    return curve.IsClosable(tolerance)


def IsCurveClosed( object_id ):
    curve = rhutil.coercecurve(object_id)
    if curve is None: return scriptcontext.errorhandler()
    return curve.IsClosed


def IsCurveInPlane( object_id, plane=None ):
  """
  Test a curve to see if it lies in a specific plane
  Parameters:
    object_id = the object's identifier
    plane[opt] = plane to test. If omitted, the active construction plane is used
  Returns:
    True or False indicating success or failure
  """
  curve = rhutil.coercecurve(object_id)
  if curve is None: return False
  if plane is None:
      plane = scriptcontext.doc.Views.ActiveView.ActiveViewport.ConstructionPlane()
  else:
      plane = rhutil.coerceplane(plane)
      if plane is None: return False
  return curve.IsInPlane(plane, scriptcontext.doc.ModelAbsoluteTolerance)


def IsCurveLinear( object_id, segment_index=-1 ):
  """
  Verifies an object is a linear curve
  Parameters:
    curve_id = identifier of the curve object
    segment_index [opt] = the curve segment if curve_id identifies a polycurve
  Returns:
    True or False indicating success or failure
  """
  curve = rhutil.coercecurve(object_id, segment_index)
  return curve and curve.IsLinear()


def IsCurvePeriodic( curve_id, segment_index=-1 ):
    """
    Verifies an object is a periodic curve object
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    return curve and curve.IsPeriodic


def IsCurvePlanar( curve_id, segment_index=-1 ):
    """
    Verifies an object is a planar curve
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    tol = scriptcontext.doc.ModelAbsoluteTolerance
    return curve and curve.IsPlanar(tol)


def IsCurveRational( curve_id, segment_index=-1 ):
    """
    Verifies an object is a rational NURBS curve
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve and isinstance(curve, Rhino.Geometry.NurbsCurve):
        return curve.IsRational
    return False


def IsEllipse( object_id ):
    """
    Verifies an ibject is an elliptical-shaped curve
    Parameters:
      curve_id = identifier of the curve object
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(object_id, segment_index)
    return curve and curve.IsEllipse()


def IsLine( object_id, segment_index=-1 ):
    """
    Verifies an object is a line curve
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(object_id, segment_index)
    return isinstance(curve, Rhino.Geometry.LineCurve)


def IsPointOnCurve( object_id, point, segment_index=-1 ):
    """
    Verifies that a point is on a curve
    Parameters:
      curve_id = identifier of the curve object
      point = the test point
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(object_id, segment_index)
    point = rhutil.coerce3dpoint(point)
    if curve is None or point is None: return scriptcontext.errorhandler()
    rc, t = curve.ClosestPoint(point, Rhino.RhinoMath.SqrtEpsilon)
    return rc


def IsPolyCurve( object_id, segment_index=-1 ):
    """
    Verifies an object is a PolyCurve curve
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(object_id, segment_index)
    return isinstance(curve, Rhino.Geometry.PolyCurve)


def IsPolyline( object_id, segment_index=-1 ):
    """
    Verifies an object is a Polyline curve object
    Parameters:
      curve_id = identifier of the curve object
      segment_index [opt] = the curve segment if curve_id identifies a polycurve
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(object_id, segment_index)
    return isinstance(curve, Rhino.Geometry.PolylineCurve)


def JoinCurves( object_ids, delete_input=False, tolerance=None ):
    """
    Joins multiple curves together to form one or more curves or polycurves
    Parameters:
      object_ids = list of identifiers of multiple curve objects
      delete_input[opt] = delete input objects after joining
      tolerance[opt] = join tolerance. If omitted, 2.1 * document absolute
          tolerance is used
    Returns:
      List of Guids representing the new curves on success
      None on error
    """
    if len(object_ids)<2: return scriptcontext.errorhandler()
    curves = []
    for id in object_ids:
        curve = rhutil.coercecurve(id)
        if curve: curves.append(curve)
    if tolerance is None:
        tolerance = 2.1 * scriptcontext.doc.ModelAbsoluteTolerance
    newcurves = Rhino.Geometry.Curve.JoinCurves(curves, tolerance)
    rc = []
    if newcurves:
        rc = [scriptcontext.doc.Objects.AddCurve(crv) for crv in newcurves]
    if not rc: return scriptcontext.errorhandler()
    if delete_input:
        for id in object_ids:
            id = rhutil.coerceguid(id)
            if id: scriptcontext.doc.Objects.Delete(id, False)
    scriptcontext.doc.Views.Redraw()
    return rc


def LineFitFromPoints(points):
    """
    Returns a line that was fit through an array of 3D points
    Parameters:
      points = a list of at least two 3D points
    Returns:
      line on success
      None on error
    """
    points = rhutil.coerce3dpointlist(points)
    if( points==None ): return scriptcontext.errorhandler()
    rc, line = Rhino.Geometry.Line.TryFitLineToPoints(points)
    if rc: return line
    return scriptcontext.errorhandler()


def MakeCurveNonPeriodic( curve_id, delete_input=False ):
    """
    Makes a periodic curve non-periodic. Non-periodic curves can develop
    kinks when deformed
    Parameters:
      curve_id = identifier of the curve object
      delete_input[opt] = delete the input curve
    Returns:
      id of the new or modified curve if successful
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None or not curve.IsPeriodic:
        return scriptcontext.errorhandler()
    nc = curve.ToNurbsCurve()
    if nc is None: return scriptcontext.errorhandler()
    nc.Knots.ClampEnd( Rhino.Geometry.CurveEnd.Both )
    rc = None
    objref = Rhino.DocObjects.ObjRef(rhutil.coerceguid(curve_id))
    if delete_input:
        rc = scriptcontext.doc.Objects.Replace(objref, nc)
        if not rc: return scriptcontext.errorhandler()
        rc = rhutil.coerceguid(curve_id)
    else:
        rc = scriptcontext.doc.Objects.AddCurve(nc, objref.Object().Attributes)
        if rc==System.Guid.Empty: return scriptcontext.errorhandler()
    objref.Dispose()
    scriptcontext.doc.Views.Redraw()
    return rc


def MeshPolyline( polyline_id ):
    """
    Creates a polygon mesh object based on a closed polyline curve object.
    The newly created mesh object is added to the document
    Parameters:
      polyline_id = identifier of the polyline curve object
    Returns:
      identifier of the new mesh object
      None on error
    """
    curve = rhutil.coercecurve(polyline_id)
    if curve is None: return scriptcontext.errorhandler()
    mesh = Rhino.Geometry.Mesh.CreateFromPlanarBoundary(curve)
    if mesh is None: return scriptcontext.errorhandler()
    rc = scriptcontext.doc.Objects.AddMesh(mesh)
    scriptcontext.doc.Views.Redraw()
    return rc


def OffsetCurve( object_id, direction, distance, normal=None, style=1 ):
    """
    Offsets a curve by a distance. The offset curve will be added to Rhino
    Parameters:
      object_id = identifier of a curve object
      direction = point describing direction of the offset
      distance = distance of the offset
      normal[opt] = normal of the plane in which the offset will occur.
          If omitted, the normal of the active construction plane will be used
      style[opt] = the corner style
          0 = None
          1 = Sharp
          2 = Round
          3 = Smooth
          4 = Chamfer
    Returns:
      List of ids for the new curves on success
      None on error
    """
    curve = rhutil.coercecurve(object_id)
    direction = rhutil.coerce3dpoint(direction)
    if curve is None or direction is None: return scriptcontext.errorhandler()
    if normal is None:
        normal = scriptcontext.doc.Views.ActiveView.ActiveViewport.ConstructionPlane().Normal
    else:
        normal = rhutil.coerce3dvector(normal)
        if normal is None: return scriptcontext.errorhandler()
    tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    style = System.Enum.ToObject(Rhino.Geometry.CurveOffsetCornerStyle, style)
    curves = curve.Offset(direction, normal, distance, tolerance, style)
    if curves is None: return scriptcontext.errorhandler()
    rc = [scriptcontext.doc.Objects.AddCurve(curve) for curve in curves]
    scriptcontext.doc.Views.Redraw()
    return rc


def OffsetCurveOnSurface( curve_id, surface_id, distance_or_parameter ):
    """
    Offset a curve on a surface. The source curve must lie on the surface. The offset curve or
    curves will be added to Rhino
    Parameters:
      curve_id, surface_id = curve and surface identifiers
      distance_or_parameter = If a single number is passed, then this is the distance of the offset.
        Based on the curve's direction, a positive value will offset to the left and a negative
        value will offset to the right.
        If a tuple of two values is passed, this is interpreted as the surface U,V parameter that the
        curve will be offset through
    Returns:
      Identifiers of the new curves if successful
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    surface = rhutil.coercesurface(surface_id)
    if curve is None or surface is None: return scriptcontext.errorhandler()
    x = None
    if( type(distance_or_parameter) is list or type(distance_or_parameter) is tuple ):
        x = Rhino.Geometry.Point2d( distance_or_parameter[0], distance_or_parameter[1] )
    else:
        x = float(distance_or_parameter)
    tol = scriptcontext.doc.ModelAbsoluteTolerance
    curves = curve.OffsetOnSurface(surface, x, tol)
    if curves is None: return scriptcontext.errorhandler()
    rc = [scriptcontext.doc.Objects.AddCurve(curve) for curve in curves]
    if not rc: return scriptcontext.errorhandler()
    scriptcontext.doc.Views.Redraw()
    return rc


def PlanarClosedCurveContainment( curve_a, curve_b, plane=None, tolerance=None ):
    """
    Determines the relationship between the regions bounded by two coplanar
    simple closed curves
    Paramters:
      curve_a, curve_b = identifiers of two planar, closed curves
      plane[opt] = test plane. If omitted, the currently active construction
        plane is used
      tolerance[opt] = if omitted, the document absolute tolerance is used
    Returns:
      a number identifying the relationship if successful
        0 = the regions bounded by the curves are disjoint
        1 = the two curves intersect
        2 = the region bounded by curve_a is inside of curve_b
        3 = the region bounded by curve_b is inside of curve_a
      None if not successful
    """
    curve_a = rhutil.coercecurve(curve_a)
    curve_b = rhutil.coercecurve(curve_b)
    if curve_a is None or curve_b is None: return scriptcontext.errorhandler()
    if tolerance is None or tolerance<=0:
        tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    plane = rhutil.coerceplane(plane)
    if plane is None:
        plane = scriptcontext.doc.Views.ActiveView.ActiveViewport.ConstructionPlane()
    rc = Rhino.Geometry.Curve.PlanarClosedCurveContainmentTest(curve_a, curve_b, plane, tolerance)
    return rc


def PointInPlanarClosedCurve( point, curve, plane=None, tolerance=None ):
    """
    Determines if a point is inside of a closed curve, on a closed curve, or
    outside of a closed curve
    Parameters:
      point = text point
      curve = identifier of a curve object
      plane[opt] = plane containing the closed curve and point. If omitted,
          the currently active construction plane is used
      tolerance[opt] = it omitted, the document abosulte tolerance is used
    Returns:
      number identifying the result if successful
          0 = point is outside of the curve
          1 = point is inside of the curve
          2 = point in on the curve
      None on error
    """
    point = rhutil.coerce3dpoint(point)
    curve = rhutil.coercecurve(curve)
    if point is None or curve is None: return scriptcontext.errorhandler()
    if tolerance is None or tolerance<=0:
        tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    plane = rhutil.coerceplane(plane)
    if plane is None:
        plane = scriptcontext.doc.Views.ActiveView.ActiveViewport.ConstructionPlane()
    rc = curve.Contains(point, plane, tolerance)
    if( rc==Rhino.Geometry.PointContainment.Unset ): return scriptcontext.errorhandler()
    if( rc==Rhino.Geometry.PointContainment.Outside ): return 0
    if( rc==Rhino.Geometry.PointContainment.Inside ): return 1
    return 2


def PolyCurveCount( curve_id, segment_index=-1 ):
    """
    Returns the number of curve segments that make up a polycurve on success
    None on error
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if isinstance(curve, Rhino.Geometry.PolyCurve): return curve.SegmentCount
    return scriptcontext.errorhandler()


def PolylineVertices( curve_id, segment_index=-1 ):
    """
    Returns the vertices of a polyline curve on success or None on error
    """
    curve = rhutil.coercecurve(curve_id, segment_index)
    if curve is None: return scriptcontext.errorhandler()
    rc, polyline = curve.TryGetPolyline()
    if rc: return [pt for pt in polyline]
    return scriptcontext.errorhandler()


def ProjectCurveToMesh( curve_ids, mesh_ids, direction ):
    """
    Projects one or more curves onto one or more surfaces or meshes
    Parameters:
      curve_ids = identifiers of curves to project
      mesh_ids = identifiers of meshes to project onto
      direction = projection direction
    Returns:
      list of identifiers on success
      None on error
    """
    curve_ids = rhutil.coerceguidlist(curve_ids)
    mesh_ids = rhutil.coerceguidlist(mesh_ids)
    direction = rhutil.coerce3dvector(direction)
    if curve_ids is None or mesh_ids is None:
        return scriptcontext.errorhandler()
    curves = []
    for id in curve_ids:
        curve = rhutil.coercecurve(id)
        if curve: curves.append(curve)
    meshes = []
    for id in mesh_ids:
        mesh = rhutil.coercemesh(id)
        if mesh: meshes.append(mesh)
    if not curves or not meshes: return scriptcontext.errorhandler()
    tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    newcurves = Rhino.Geometry.Curve.ProjectToMesh(curves, meshes, direction, tolerance)
    if not newcurves: return scriptcontext.errorhandler()
    ids = [scriptcontext.doc.Objects.AddCurve(curve) for curve in newcurves]
    scriptcontext.doc.Views.Redraw()
    return ids


def ProjectCurveToSurface( curve_ids, surface_ids, direction ):
    """
    Projects one or more curves onto one or more surfaces or polysurfaces
    Parameters:
      curve_ids = identifiers of curves to project
      surface_ids = identifiers of surfaces to project onto
      direction = projection direction
    Returns:
      list of identifiers on success
      None on error
    """
    curve_ids = rhutil.coerceguidlist(curve_ids)
    surface_ids = rhutil.coerceguidlist(surface_ids)
    direction = rhutil.coerce3dvector(direction)
    if curve_ids is None or surface_ids is None:
        return scriptcontext.errorhandler()
    curves = []
    for id in curve_ids:
        curve = rhutil.coercecurve(id)
        if curve: curves.append(curve)
    breps = []
    for id in surface_ids:
        brep = rhutil.coercebrep(id)
        if brep: breps.append(brep)
    if not curves or not breps: return scriptcontext.errorhandler()
    tolerance = scriptcontext.doc.ModelAbsoluteTolerance
    newcurves = Rhino.Geometry.Curve.ProjectToBrep(curves, breps, direction, tolerance)
    if not newcurves: return scriptcontext.errorhandler()
    ids = [scriptcontext.doc.Objects.AddCurve(curve) for curve in newcurves]
    scriptcontext.doc.Views.Redraw()
    return ids

def RebuildCurve( curve_id, degree=3, point_count=10 ):
    """
    Rebuilds a curve to a given degree and control point count. For more
    information, see the Rhino help for the Rebuild command.
    Parameters:
      curve_id = identifier of the curve object
      degree[opt] = new degree (must be greater than 1)
      point_count [opt] = new point count, which must be bigger than degree.
    Returns:
      True of False indicating success or failure
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None or degree<=1: return False
    newcurve = curve.Rebuild(point_count, degree, False)
    if newcurve is None: return False
    objref = Rhino.DocObjects.ObjRef(curve_id)
    scriptcontext.doc.Objects.Replace(objref, newcurve)
    objref.Dispose()
    scriptcontext.doc.Views.Redraw()
    return True


def ReverseCurve( curve_id ):
    """
    Reverses the direction of a curve object. Same as Rhino's Dir command
    Parameters:
      curve_id = identifier of the curve object
    Returns:
      True or False indicating success or failure
    """
    curve = rhutil.coercecurve(curve_id)
    if curve and curve.Reverse():
      curve_id = rhutil.coerceguid(curve_id)
      objref = Rhino.DocObjects.ObjRef(curve_id)
      scriptcontext.doc.Objects.Replace(objref, curve)
      objref.Dispose()
      return True
    return False


def SimplifyCurve( curve_id, flags=0 ):
    "Replace a curve with a geometrically equivalent polycurve"
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return False
    _flags = Rhino.Geometry.CurveSimplifyOptions.All
    if( flags&1 ==1 ): _flags = _flags - Rhino.Geometry.CurveSimplifyOptions.SplitAtFullyMultipleKnots
    if( flags&2 ==2 ): _flags = _flags - Rhino.Geometry.CurveSimplifyOptions.RebuildLines
    if( flags&4 ==4 ): _flags = _flags - Rhino.Geometry.CurveSimplifyOptions.RebuildArcs
    if( flags&8 ==8 ): _flags = _flags - Rhino.Geometry.CurveSimplifyOptions.RebuildRationals
    if( flags&16==16 ): _flags = _flags - Rhino.Geometry.CurveSimplifyOptions.AdjustG1
    if( flags&32==32 ): _flags = _flags - Rhino.Geometry.CurveSimplifyOptions.Merge
    tol = scriptcontext.doc.ModelAbsoluteTolerance
    ang_tol = scriptcontext.doc.ModelAngleToleranceRadians
    newcurve = curve.Simplify( _flags, tol, ang_tol )
    if newcurve:
        curve_id = rhutil.coerceguid(curve_id)
        objref = Rhino.DocObjects.ObjRef(curve_id)
        scriptcontext.doc.Objects.Replace(objref, newcurve)
        objref.Dispose()
        scriptcontext.doc.Views.Redraw()
        return True
    return False

def SplitCurve( curve_id, parameter, delete_input=True ):
    """
    Splits, or divides, a curve at a specified parameter. The parameter must
    be in the interior of the curve's domain
    Parameters:
      curve_id = identifier of the curve object
      parameter = one or more parameters to split the curve at
      delete_input[opt] = delete the input curve
    Returns:
      list of new curve ids on success
      None on error
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None: return scriptcontext.errorhandler()
    newcurves = curve.Split(parameter)
    if newcurves is None: return scriptcontext.errorhandler()
    objref = Rhino.DocObjects.ObjRef(rhutil.coerceguid(curve_id))
    att = objref.Object().Attributes
    rc = [scriptcontext.doc.Objects.AddCurve(crv, att) for crv in newcurves]
    if not rc: return scriptcontext.errorhandler()
    if delete_input: scriptcontext.doc.Objects.Delete(objref, True)
    scriptcontext.doc.Views.Redraw()
    return rc


def TrimCurve( curve_id, interval, delete_input=True ):
    """
    Trims a curve by removing portions of the curve outside the specified interval
    Paramters:
      curve_id = identifier of the curve object
      interval = two numbers indentifying the interval to keep. Portions of
        the curve before domain[0] and after domain[1] will be removed. If the
        input curve is open, the interval must be increasing. If the input
        curve is closed and the interval is decreasing, then the portion of
        the curve across the start and end of the curve is returned
      delete_input[opt] = delete the input curve
    Reutrns:
      identifier of the new curve on success
      None on failure
    """
    curve = rhutil.coercecurve(curve_id)
    if curve is None or interval[0]==interval[1]: return scriptcontext.errorhandler()
    newcurve = curve.Trim(interval[0], interval[1])
    if newcurve is None: return scriptcontext.errorhandler()
    objref = Rhino.DocObjects.ObjRef(rhutil.coerceguid(curve_id))
    att = objref.Object().Attributes
    rc = scriptcontext.doc.Objects.AddCurve(newcurve, att)
    if( delete_input ): scriptcontext.doc.Objects.Delete(objref, True)
    scriptcontext.doc.Views.Redraw()
    return rc