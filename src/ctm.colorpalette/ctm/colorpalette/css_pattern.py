# -*- encoding: utf-8 -*-
from colorsys import *
from colorops import RGBColor

def obtainPalette(color):
	color = '0x'+color
	color = int(color, 16)
	color = RGBColor(color)
	(r, g, b) = color.get_rgb()
	(h, s, v) = rgb_to_hsv(r/255.0, g/255.0, b/255.0)
	s_step = (0-s)/10.0
	# Canviar aqui si volem que el degradat vagi cap a 
	# un altre color, per exemple blanc o gris
	v_step = ((0xFF/255.0)-v)/10.0 
	L = []
	contrast_color1 = color.contrast_color(colors=(0x000000, 0xFFFFFF))
	for a in range(11):
		ss = s+s_step*a
		vv = v+v_step*a
		(r, g, b) = hsv_to_rgb(h, ss, vv)
		color2 = RGBColor(0)
		color2.set_rgb((r*255, g*255, b*255))
		result = "#"+str(color2)
		L.append(result)
	color3 = RGBColor(str(L[4]))
	contrast_color2 = color3.contrast_color(colors=(0xFFFFFF, color, 0x000000))
	return (L[0], L[4], L[8], "#"+str(contrast_color1), "#"+str(contrast_color2)) 


CTM_CSS=u"""
/* ------------- CORRECCIONS ICONES -------------- */

body table.listing a {
    display: inline;
}

/* ------------- ESTILS GENERALS ----------------- */

/*Color dels links al Portal Site Actions*/
#portal-siteactions a:link, #portal-siteactions a:visited {
    color: %(nivell1)s;
}

/* ------------- PORTAL HEADER ----------------- */
/*Imatge de fons de la capçalera*/

body #ctm-logo div {
    background-image: url("%(logo)s");
    width: %(logowidth)spx;
    height: %(logoheight)spx;
}

body #portal-header {
    background-image: %(background_image)s';
}

body #ctm-logo {
    display: inline-block;
    margin: 1em 0;
}

body .searchSection {
    color: %(nivell1)s; /*o oposat...*/
}


/* ------------- PORTAL GLOBALNAV ----------------- */

/*El background del portal-globalnav*/
body #portal-globalnav {
    background: %(nivell2)s;
}

/*Els que no estan seleccionats*/
body #portal-globalnav li a {
    background: %(nivell2)s;
    color: %(links2)s;
}

/*Quan passes per sobre dun seleccionat, canvia a laspecte dels no selected*/
body #portal-globalnav .selected a:hover {
    background: %(nivell2)s;
    color: %(links2)s;
}

/*Els que estan seleccionats o quan passes el ratoli per sobre*/
body #portal-globalnav .selected a, body #portal-globalnav a:hover {
    background: %(nivell1)s;
    color: %(links1)s;
}
/* ------------- PORTAL FOOTER ----------------- */

/*Color del portal footer*/
body #portal-footer {
    background: %(footer_bg)s;
}

/*Alineacio del text centrat del p-footer*/
body #portal-footer p{
    text-align: center;
}


/* ------------- PERSONAL TOOLS ----------------- */

/*Pel que fa al color del personaltools, afecta el css corresponent
als links*/

body #portal-personaltools {
    background: %(nivell2)s;
}

body #portal-personaltools dd{
    background: %(nivell2)s;
}

body #portal-personaltools dd a:hover {
    background: %(nivell1)s;
    color: %(links1)s;
}

body #portal-personaltools dd a{
   color: %(links2)s;
}

#portal-personaltools dt.actionMenuHeader a {
   color: %(links2)s;
}


body #portal-personaltools #anon-personalbar a {
    color: %(links2)s;
}

/* ------------- PORTLETS ----------------- */

/*Portlet manager*/

body .ploneCalendar .weekdays th {
    background: %(nivell3)s;
}

body .managePortletsLink a:link, body .managePortletsLink a:visited {
    color: %(links2)s;
}

body dl.portlet dt, body div.portletAssignments div.portletHeader {
    background: %(nivell2)s;
    color: %(links2)s;
}


body dl.portlet dt a:link, body dl.portlet dt a:visited, body dl.portlet dt a:hover {
   color: %(links2)s;
}


/*Botonet de Administrar Portlets*/
body div.managePortletsLink, body a.managePortletsFallback {
    background: %(nivell2)s;
    color: %(links2)s;
}


body dl.portlet dd.portletItem, body dl.portlet dd.portletFooter, body dl.portletError dd {
    background-color: %(portlets_bg)s;
}

/* ------------- Afegits per compatibilitzar amb Plone DropDown Menu 1.2.12  ----------------- */

/*És el que està clicat però no hi ha el ratolí a sobre*/
body #portal-globalnav li.selected a {
    background-color: %(nivell1)s;
    color: %(links1)s;
}


/*Quan has seleccionat una pestanya que té fills, els d'asota quan no passes per sobre es veuen així*/
body #portal-globalnav li.selected ul li a {
    background-color: %(nivell2)s;
    color: %(links2)s;
}

/*Aquest és quan passes per sobre, independentment que estigui seleccionat o no*/
body #portal-globalnav:hover li:hover > a {
    background-color: %(nivell1)s;
    color: %(links1)s;
}

/*Quan no esta seleccionat i passes per sobre un que té subcarpetes, aquestes es veuen del color que es defineixi aqui*/
body #portal-globalnav ul li a {
    background-color: %(nivell2)s;
    color: %(links2)s;
}


body #portal-globalnav ul li a.hasChildrens {
    background-color: %(nivell2)s;
    color: %(links2)s;
}

body #portal-globalnav ul li a.hasChildrens:hover {
    background-color: %(nivell1)s;
    color: %(links1)s;
}


/*----- Aquests no es veu el seu efecte -----*/

body #portal-globalnav:hover li:hover ul > a {
    background-color:#000000;
    color: #000000;
}

"""
