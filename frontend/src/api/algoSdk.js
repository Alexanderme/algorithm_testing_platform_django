import request from '@/utils/request'

export function getPackageIas(formData) {
  return request({
    url: 'sdk/iasPackage',
    method: "post",
    data: formData,
  })
}


export function getPackageVas(formData) {
  return request({
    url: 'sdk/vasPackage',
    method: "post",
    data: formData,
  })
}


export function getSdkOpenCV(formData) {
  return request({
    url: 'api/sdk/algoMessage',
    method: "post",
    data: formData,
  })
}

export function postAlgoFilesResult(formData) {
  return request({
    url: 'sdk/algoRes',
    method: "post",
    data: formData,
  })
}

export function getAlgoFiles(formData) {
  return request({
    url: 'sdk/fileResult',
    method: "post",
    responseType: "arraybuffer",
    data: formData
  })
}


export function getAlgoFilesTaskId(formData) {
  return request({
    url: 'sdk/taskInfo',
    method: "get",
    data: formData
  })
}

export function clearAlgoRunEnv(formData) {
  return request({
    url: 'sdk/cleanEnv',
    method: "post",
    data: formData
  })
}


// // data_set
// export function AlgoDataSetFormatXml(formData) {
//   return request({
//         url: 'algo_sdk/format_xml',
//         method:"post",
//         data:formData,
//         responseType: "arraybuffer",
//     })
// }
//
// export function AlgoDataSetFormatImage(formData) {
//   return request({
//         url: 'algo_sdk/image_data_set',
//         method:"post",
//         data:formData
//     })
// }
//
// export function getAlgoDataSetTaskId(params) {
//   return request({
//         url: 'algo_sdk/data_set_taskstatus',
//         method:"get",
//         params
//     })
// }

// export function getChangeXmlTag(formData) {
//   return request({
//         url: 'algo_sdk/change_xml_tag',
//         method:"post",
//         data:formData,
//         responseType: "arraybuffer",
//     })
// }
//
//
//
// export function clearDataSetEnv(formData) {
//   return request({
//         url: 'algo_sdk/data_set_clean_env',
//         method:"post",
//         data:formData
//     })
// }

//miss_rate

export function getMissRateTaskId(params) {
  return request({
    url: 'sdk/taskInfo',
    method: "get",
    params
  })
}


export function getAlgoPrecision(formData) {
  return request({
    url: 'sdk/algoPerssion',
    method: "post",
    data: formData
  })
}

// // performamce
//
// export function getAlgoResourceOccupation(formData) {
//     return request({
//         url: 'algo_sdk/resource_occupation',
//         method:"post",
//         data:formData
//     })
// }
