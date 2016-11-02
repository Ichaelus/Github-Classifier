# API

## Base url

Alle Abfragen werden via `GET` an den host `http://classifier.leimstaedtner.it/ajax.php` gesendet. Das Attribut `key` unterscheidet dann die gewünschte Grundmenge, `filter` dient zur Verfeinerung der Resultate.

**Beispiel-Url:**
`http://classifier.leimstaedtner.it/ajax.php?key=api:all&filter=Y2xhc3M9REVWfEhXLHN0YXJzPjM=`

## Key Attribute

### api:all

Gibt ungefiltert alle Datensätze aus.

### api:equal

Gibt je Klasse gleich viele Datensätze zurück.

### api:count

Liefert die Anzahl der betroffenen Datensätzen.

### api:class

Ein Shortcut for api:all mit entsprechenden Class Filter. Anwendung:
`/?key=api:class&name=CLASSNAME`

### api:class-count

Kombination der obigen. Liefert die Anzahl der Samples pro Klasse zurück.


## Filtern

Das `filter` Attribut kann, wenn gesetzt, mit einem **base 64 encodierten** Array der Form [attribut1=wert1,...] gefüllt werden. Neben dem Operator `=` können, wenn sinnvoll, auch die Operatoren `<, <=, >, >=` verwendet werden.
Werden verschiedene Attributfilter mit einem `,` getrennt, resultiert das in eine **AND** Verknüpfung. Will man hingegen eine **OR** Verknüfung, reicht es ein `|` Symbol anstelle des Kommas zu verwenden. (OR bindet hier stärker(!) als AND).

**Beispiel**
```javascript 
btoa("class=DEV|HW,stars>3");
```
erzeugt den Filter-Wert der obigen Beispiel-Url. Das SQL Äquivalent ist:

```sql
SELECT ... WHERE  ( `class` = 'DEV' OR `class` = 'HW' ) AND  ( `stars` > '3' )
```

Mögliche Filterattribute:
<table>
	<thead>
		<tr>
			<th>Name</th>
			<th>Operatoren</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>author</td>
			<td>=</td>
		</tr>
		<tr>
			<td>class</td>
			<td>=</td>
		</tr>
		<tr>
			<td>description</td>
			<td>=</td>
		</tr>
		<tr>
			<td>forks</td>
			<td><,<=,=,>=,></td>
		</tr>
		<tr>
			<td>id</td>
			<td><,<=,=,>=,></td>
		</tr>
		<tr>
			<td>languages</td>
			<td>=</td>
		</tr>
		<tr>
			<td>name</td>
			<td>=</td>
		</tr>
		<tr>
			<td>readme</td>
			<td>=</td>
		</tr>
		<tr>
			<td>stars</td>
			<td><,<=,=,>=,></td>
		</tr>
		<tr>
			<td>tree</td>
			<td>=</td>
		</tr>
		<tr>
			<td>url</td>
			<td>=</td>
		</tr>
		<tr>
			<td>watches</td>
			<td><,<=,=,>=,></td>
		</tr>
	</tbody>
</table>
