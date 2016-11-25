# API

## Base url

Alle Abfragen werden via `GET` an den host `http://classifier.leimstaedtner.it/ajax.php` gesendet. Das Attribut `key` unterscheidet dann die gewünschte Grundmenge, `filter` dient zur Verfeinerung der Resultate.

**Beispiel-Url:**
`http://classifier.leimstaedtner.it/ajax.php?key=api:all&filter=Y2xhc3M9REVWfEhXLHN0YXJzPjM=`

### ?key=api:train

Gibt alle Datensätze der Tabelle train aus.

### ?key=api:test

Gibt alle Datensätze der Tabelle test aus.

### ?key=api:unlabeled

Gibt alle Datensätze der Tabelle unlabeled aus.

### ?key=api:to_classify

Gibt alle Datensätze der Tabelle train aus.

## Weitere Funktionen

_Für viele der folgenden Funktionen kann ein Attribut `table` {train, test, unlabeled, to_classify} bzw. das unten erläuterte `filter` Attribut gesetzt werden.

### ?key=api:single

Gibt einen zufälligen klassifizierten Datensatz zurück. (Attribute: `table`)

### ?key=api:equal

Gibt je Klasse gleich viele Datensätze zurück. (Attribute: `table`)

### ?key=api:class

Ein Shortcut for api:all mit entsprechenden Class Filter. (Attribute: `table`, `name`). Anwendung:
`/?key=api:class&name=CLASSNAME`

### ?key=api:count

Liefert die Anzahl der betroffenen Datensätzen.(Attribute: `table`, `filter`)

### ?key=api:class-count

Kombination der obigen. Liefert die Anzahl der Samples pro Klasse zurück.(Attribute: `table`, `filter`)

### ?key=api:tagger-class-count

Liefert die Anzahl der Samples pro Klasse zurück, beschränkt auf einen angegebenen `tagger`. (Attribute: `table`, `tagger`)

### ?key=api:generate_sample_url

Gibt die API-Url eines **zufälligen** Github repositorys  zurück.

`client_id` und `client_secret` können übergeben werden, ansonsten werden gespeicherte credentials verwendet.

### ?key=api:generate_sample

Diese Funktion ist vom Parameter `api-url` abhängig. Für das angegebene repository wird damit ein ungelabelter Datenbankeitnrag bzw. Klassifikationsvektor generiert und im JSON Format ausgegeben. Ist `api-url` leer oder nicht gesetzt, wird ein zufälliges sample generiert. Wird ein zweiter, auch optionaler, Paramter `class` übergeben, wird das sample direkt klassifiziert, ansonsten erhält es die Klasse `UNLABELED`.

`client_id` und `client_secret` können übergeben werden, ansonsten werden gespeicherte credentials verwendet.

## Deprecated

### ?key=api:old

Gibt alle **alten** Datensätze aus, d.h. jene mit beschränkt vielen Features.

### ?key=api:to-reclassify

Gibt einen Datensatz zurück, der in der alten Datenmenge vorhanden ist, aber noch nicht in der neuen.


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
			<th>Typ</th>
			<th>Beschreibung</th>
		</tr>
	</thead>
	<tbody>
		<tr>
	<td>api_calls</td>
	<td>Integer</td>
	<td>Number of calls needed to gather the data</td>
</tr>
<tr>
	<td>api_url</td>
	<td>String</td>
	<td>The Git-API url for this repo</td>
</tr>
<tr>
	<td>author</td>
	<td>String</td>
	<td>Repository author name</td>
</tr>
<tr>
	<td>avg_commit_length</td>
	<td>Integer</td>
	<td>Average commit message length</td>
</tr>
<tr>
	<td>branch_count</td>
	<td>Integer</td>
	<td></td>
</tr>
<tr>
	<td>class</td>
	<td>String</td>
	<td>The label given by our classifier</td>
</tr>
<tr>
	<td>commit_count</td>
	<td>Integer</td>
	<td></td>
</tr>
<tr>
	<td>commit_interval_avg</td>
	<td>Integer</td>
	<td>Average #days between two commits</td>
</tr>
<tr>
	<td>commit_interval_max</td>
	<td>Integer</td>
	<td>Maximum #days between two commits</td>
</tr>
<tr>
	<td>contributors_count</td>
	<td>Integer</td>
	<td></td>
</tr>
<tr>
	<td>description</td>
	<td>String</td>
	<td></td>
</tr>
<tr>
	<td>files</td>
	<td>String Array, separator ' '</td>
	<td>Files of the first layer</td>
</tr>
<tr>
	<td>file_count</td>
	<td>Integer</td>
	<td></td>
</tr>
<tr>
	<td>folders</td>
	<td>String Array, separator ' '</td>
	<td>Folders of the first layer</td>
</tr>
<tr>
	<td>folder_count</td>
	<td>Integer</td>
	<td></td>
</tr>
<tr>
	<td>forks</td>
	<td>Integer</td>
	<td></td>
</tr>
<tr>
	<td>hasDownloads</td>
	<td>Boolean</td>
	<td>Is the repo downloadable?</td>
</tr>
<tr>
	<td>hasWiki</td>
	<td>Boolean</td>
	<td></td>
</tr>
<tr>
	<td>id</td>
	<td>Integer</td>
	<td>Internal ID</td>
</tr>
<tr>
	<td>isFork</td>
	<td>Boolean</td>
	<td></td>
</tr>
<tr>
	<td>open_issues_count</td>
	<td>Integer</td>
	<td></td>
</tr>
<tr>
	<td>language_main</td>
	<td>String</td>
	<td>The most used language</td>
</tr>
<tr>
	<td>language_array</td>
	<td>String Array, separator ' '</td>
	<td>A list of used languages</td>
</tr>
<tr>
	<td>name</td>
	<td>String</td>
	<td>The repository title</td>
</tr>
<tr>
	<td>readme</td>
	<td>String</td>
	<td></td>
</tr>
<tr>
	<td>stars</td>
	<td>Integer</td>
	<td></td>
</tr>
<tr>
	<td>treeArray</td>
	<td>Sring Array, separator ' '</td>
	<td>A list of folder paths present in this repository</td>
</tr>
<tr>
	<td>treeDepth</td>
	<td>Integer</td>
	<td>Maximum folder depth</td>
</tr>
<tr>
	<td>url</td>
	<td>String</td>
	<td></td>
</tr>
<tr>
	<td>watches</td>
	<td>Integer</td>
	<td></td>
</tr>
	</tbody>
</table>
