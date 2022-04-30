<script>
  import { 
    Grid,
    Column,
    Row,
    Accordion,
    AccordionItem,
    DataTable,
    TooltipDefinition,
    TextInput
  } from "carbon-components-svelte";
  import TextInputGroup from "$lib/TextInputGroup.svelte";
  import Api from "../services/Api";

  let symbols = [{
    address: "",
    identifier: ""
  }];

  let results = [{
    distro: "default",
    name: "no_result",
    match: 0
  }];

  let result_details = {
    no_result: {
      hash: null,
      base_url: null,
      so_url: null
    }
  };

  let common_view = [];
  let common_keys = ["__libc_start_main_ret", "dup2", "printf", "puts", "read", "str_bin_sh", "system", "write"];

  let view = [];
  let current_view;
  let search_keyword;
  
  function checkTextInput(){
    symbols = symbols.filter(({ identifier, address }) => !(identifier == "" && address == ""));
    queryLibs();
    symbols.push({
      address: "",
      identifier: ""
    });
  }

  function deleteTextInput(event){
    symbols.splice(event.detail.id, 1);
    symbols = symbols;
    queryLibs();
  }

  function queryLibs(){
    let _symbols = {};
    Array.from(symbols).forEach((symbol) => {
      _symbols[symbol["identifier"]] = symbol["address"]
    })
    Api.post("/api/libs", JSON.stringify({symbols: _symbols})).then((response) => {
      Array.from(response).forEach((lib) => {
        result_details[lib.name] = {
          name: lib.name,
          distro: lib.distro
        };
      });
      results = response;
    });
  }

  function queryLibDetail(name){
    if(result_details[name]["base_url"] != undefined){
      return;
    }
    Api.get("/api/lib/" + name).then((response) => {
      result_details[name] = response;
      results = results;
    });
  }

  function search(keyword){
    if(keyword.toString().startsWith(":")){
      results = [{
        "distro": "",
        "name": keyword.replace(":", ""),
        "match": 1
      }];
      result_details[keyword.replace(":", "")] = {
          name: keyword.replace(":", ""),
          distro: ""
        };
    }else{
      view = [{
        id: 0,
        function: keyword,
        address: result_details[current_view]["symbols"][keyword]
      }]
    }
  }

</script>

<svelte:head>
  <title>-L- Libcヽ(✿ﾟ▽ﾟ)ノ</title>
</svelte:head>

<Grid>
  <Row>
    <Column padding>
      <h2>Address</h2>
    </Column>
    <Column padding>
      <h2>Result</h2>
    </Column>
    <Column padding>
      <h2>View</h2>
    </Column>
    <Column padding>
      <h2>Search</h2>
    </Column>
  </Row>
  <Row>
  <Column padding>
    {#each symbols as symbol, i}
      <TextInputGroup 
      bind:address={symbol.address} 
      bind:identifier={symbol.identifier}
      disabled={symbols.length === 1 || i === symbols.length - 1}
      id={i}
      on:change={checkTextInput}
      on:delete={deleteTextInput}
      ></TextInputGroup>
    {/each}
  </Column>
  <Column padding>
    <Accordion>
      {#each results as result}
        <AccordionItem
        on:click={queryLibDetail(result.name)} 
        title={result.distro + " - " + result.name + "(" + result.match + ")"}>
          {#each Object.entries(result_details[result.name]) as [key, value]}
            {#if key.indexOf("url") != -1}
            <p><a href={value} target="_blank">{key}</a></p>
            {:else if key.indexOf("symbols") != -1}
              <null></null>
            {:else if key == "name"}
              <p><b>{key}</b>: 
                <TooltipDefinition 
                tooltipText="Take it!"
                on:click={() => {
                  current_view = value;
                  common_view = [];
                  Array.from(common_keys).forEach((e, i) => {
                    common_view.push({id: i, function: e, address: result_details[value]["symbols"][e]})
                  });
                  common_view = common_view;
                }}>
                  {value}
                </TooltipDefinition>
              </p>
            {:else}
              <p><b>{key}</b>: {value}</p>
            {/if}
          {/each}
        </AccordionItem>
      {/each}
    </Accordion>
  </Column>
  <Column padding>
      <DataTable
      size="medium"
      zebra
      headers={[
          { key: "function", value: "Function" },
          { key: "address", value: "Address" }
      ]}
      rows={common_view}
      >
      </DataTable>
  </Column>
  <Column padding>
    <TextInput 
    hideLabel
    placeholder="lib/function"
    bind:value={search_keyword}
    on:change={search(search_keyword)}
    on:blur={search(search_keyword)} 
    />
    <DataTable
    size="medium"
    zebra
    headers={[
        { key: "function", value: "Function" },
        { key: "address", value: "Address" }
    ]}
    rows={view}
    >
    </DataTable>
  </Column>
  </Row>
</Grid>
