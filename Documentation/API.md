# API

## Base url

_Queries with the need of database information are always sent via `GET` to the backend host, which is by default `http://67.209.116.156/ajax.php` (a small but stable database server). Services can be accessed with the attribute `key`, results can be refined using the additional attribute `filter`, `limit`. `selector` and `table`. The server response consists of a JSON object containing a boolean `success` which determines the execution state and `data`, the query result.

THe backend host can be switched if every occurence of the IP written above is being swapped, but database integrity must be guaranteed._

**Sample-Query:**
`http://67.209.116.156/ajax.php?key=api:all&table=train&limit=5`

## Base Services

### ?key=api:all

Returns all rows of the table `table`. (attributes: `table`, `limit`(opt.), `filter` (opt.), `selector` (opt.))

### ?key=api:train

Returns all rows of the table train. (attributes: `limit`(opt.), `filter` (opt.), `selector` (opt.))

Similar calls are possibily for `api:train`,`api:test`,`api:unlabeled`,`api:to_classify`,`api:semi_supervised`,`api:standard_train_samples` and `api:standard_test_samples`.

## Additional Services

_Attributes and its possibly states are being described in the following section._

### ?key=api:single

Returns a random sample of the given `table`. (attributes: `table`. `selector` (opt.))

### ?key=api:equal

Returns an equal amount of samples based on the class count of the given table. (attributes: `table`)

### ?key=api:class

Returns all samples of the given class `name`. (attributes: `table`, `name`, `selector` (opt.)).

Application:
`/?key=api:class&name=CLASSNAME`

### ?key=api:count

Returns the amount of rows affected by `table` and `filter`. (attributes: `table`, `filter`)

### ?key=api:class-count

Combination of the two above. Returns the a class-based row count. (attributes: `table`, `filter`)

### ?key=api:tagger-class-count

Returns the a class-based row count, limitated to the given `tagger`. Used to see how many samples have been classified by a single person. (attributes: `table`, `tagger`)

### ?key=api:move

Moves a repository, taken from the pool `from_table` to the pool `to_table`. If `label` is set, the label of the sample will be changed.
The attribute `api-url` must be passed as an identifier. (attributes: `from_table`, `to_table`, `api_url`, `label` (opt.))

## Services dependend on the GitHub API

### ?key=api:generate_sample_url

Generates and returns the API-url of a **random** GitHub repository.

Attributes `client_id` and `client_secret` can (but mustn't) be passed in order ot be used by the server. If they aren't, hardcoded credentials will be used with their limitation of 5000 API calls per minute.

### ?key=api:generate_sample

This service depends on the parameter `api_url`. Feature extraction and accordingly data dumping to the database is being made for the given repository. The unlabeled row is being saved and returned to the client.
If the parameter `api-url` is empty, a random sample is being generated. The attribute `class` (opt.) leads to an instant classification of the sample, if empty the class `UNLABELED` is being used.

Attributes `client_id` and `client_secret` can (but mustn't) be passed in order ot be used by the server.


## Attributes

The most essential attribute is `table`, its value defines the database table on which the query is being executed. Possible values are:

<table>
	<thead>
		<tr>
			<th>Table Name</th>
		</tr>
	</thead>
	<tbody>
		<tr><td>unlabeled</td></tr>
		<tr><td>train</td></tr>
		<tr><td>test</td></tr>
		<tr><td>to_classify</td></tr>
		<tr><td>standard_train_samples</td></tr>
		<tr><td>standard_test_samples</td></tr>
	</tbody>
</table>

To keep queries efficient, the attribute `selector` determines which columns should be returned. If emty, '*' will be used.

Example: `selector=class, api_url`

SQL equivalent: `SELECT class, api_url FROM ...`

The paramter `limit` defines the maximum amount of result data samples, which are being chosen randomly.

The attribute `filter` can be set to (if supported by the service) a **base 64 encoded** array structured like `[attr1=val1,..]`. Operators available are `=`, `<`, `<=`, `>` and `>=`. Pairs of attribute specific filters can be seperated either with `,`, which results in an **AND** conjunction or with `|` which forms an **OR** disjunction. (In our case, OR binds stronger(!) than AND).

**Example**
```javascript 
btoa("class=DEV|HW,stars>3");
```
generates a possible `filter` value (in JS). The SQL equivalent is:

```sql
SELECT ... WHERE  ( `class` = 'DEV' OR `class` = 'HW' ) AND  ( `stars` > '3' )
```

Possible filter attributes (Or: the general table structure):
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
