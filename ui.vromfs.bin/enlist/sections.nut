from "%enlSqGlob/ui_library.nut" import *

let { isNewDesign } = require("%enlSqGlob/designState.nut")
let mainScreenUi = isNewDesign.value
  ? require("%enlist/mainScene/mainScene.nut")
  : require("soldiers/soldiersList.ui.nut")

let shopUi = isNewDesign.value
  ? require("shop/shopUi.nut")
  : require("shop/armyShopUi.nut")

let researchesUi = isNewDesign.value
  ? require("researches/researchesUi.nut")
  : require("researches/researchesList.ui.nut")

let squadSoldiersUi = require("%enlist/squad/squadSoldiersUi.nut")

let armyUnlocksUi = require("soldiers/armyUnlocksUi.nut")
let { mkNotifierBlink, mkNotifierNoBlink } = require("%enlist/components/mkNotifier.nut")
let {
  setSectionsSorted, curSection, mainSectionId
} = require("%enlist/mainMenu/sectionsState.nut")
let {
  seenResearches, markSeen, curUnseenResearches
} = require("researches/unseenResearches.nut")
let { isCurCampaignProgressUnlocked } = require("%enlist/meta/curCampaign.nut")
let {
  curUnseenAvailShopGuids, hasUnseenCurrencies, isShopVisible, hasShopSection,
  curArmyShopItems, notOpenedShopItems
} = require("shop/armyShopState.nut")
let { nextTutorialUnlock, showGetUnlockTutorial
} = require("%enlist/tutorial/notReceivedUnlockTutorial.nut")
let { hasCampaignSection } = require("soldiers/model/armyUnlocksState.nut")
let { hasLevelDiscount, curLevelDiscount
} = require("%enlist/campaigns/armiesConfig.nut")
let { curArmyData } = require("%enlist/soldiers/model/state.nut")
let openUrl = require("%ui/components/openUrl.nut")
let { getStoreUrl, getEventUrl} = require("%ui/networkedUrls.nut")
let { isEventUnseen, markEventSeen } = require("gameModes/eventUnseenSignState.nut")
let { markShopItemOpened } = require("%enlist/shop/unseenShopItems.nut")
let { seenArmyProgress, markOpened } = require("%enlist/soldiers/model/unseenArmyProgress.nut")
let { discountBgColor } = require("%enlSqGlob/ui/viewConst.nut")
let { defTxtColor, accentColor } = require("%enlSqGlob/ui/designConst.nut")


let function researchesAlertUi() {
  let { hasUnseen = false, hasUnopened = false } = curUnseenResearches.value
  let mkNotifier = hasUnopened ? mkNotifierBlink : mkNotifierNoBlink
  return {
    watch = curUnseenResearches
    hplace = ALIGN_RIGHT
    pos = [0, hdpx(30)]
    children = !hasUnseen ? null
      : mkNotifier(loc("hint/newResearchesAvailable"))
  }
}

let hasUnseenShopItems = Computed(@() hasUnseenCurrencies.value
  || curUnseenAvailShopGuids.value.len() > 0)

let maxCurArmyDiscount = Computed(function() {
  let lvl = curArmyData.value?.level ?? 0
  return curArmyShopItems.value.reduce(@(res, val)
    (val?.requirements.armyLevel ?? 0) > lvl
      ? res
      : max(res, (val?.hideDiscount ? 0 : val?.discountInPercent ?? 0)), 0)
})

let haveSpecialOfferArmy = Computed(function() {
  return curArmyShopItems.value.findvalue(@(val)
    val?.hideDiscount && (val?.discountInPercent ?? 0) > 0 && val?.showSpecialOfferText
  ) != null
})

let hasShopAlert = Computed(@() hasShopSection.value
  && isCurCampaignProgressUnlocked.value
  && isShopVisible.value
  && (maxCurArmyDiscount.value > 0 || hasUnseenShopItems.value))

let discountBg = { color = discountBgColor }

let shopAlertBlink = Computed(@()
  curSection.value != "SHOP"
    && (notOpenedShopItems.value.len() > 0 || maxCurArmyDiscount.value > 0))

let function shopAlertUi() {
  let mkNotifier = shopAlertBlink.value ? mkNotifierBlink : mkNotifierNoBlink
  let percents = maxCurArmyDiscount.value
  let children = percents > 0
      ? mkNotifier(loc("shop/discount", { percents }), {}, discountBg)
    : haveSpecialOfferArmy.value
      ? mkNotifier(loc("specialOfferShort"))
    : hasShopAlert.value
      ? mkNotifier(loc("hint/newShopItemsAvailable"))
    : null
  return {
    watch = [hasShopAlert, maxCurArmyDiscount, shopAlertBlink, haveSpecialOfferArmy]
    hplace = ALIGN_RIGHT
    pos = [0, hdpx(30)]
    children
  }
}

let hasUnseenArmyProgress = Computed(@() hasCampaignSection.value
  && isCurCampaignProgressUnlocked.value
  && curArmyData.value?.guid in seenArmyProgress.value?.unseen
)
let hasUnopenedArmyProgress = Computed(@() hasCampaignSection.value
  && isCurCampaignProgressUnlocked.value
  && curArmyData.value?.guid in seenArmyProgress.value?.unopened
)


let campaignTabData = {
  locId = "menu/campaignRewards"
  descId = "menu/campaignRewardsDesc"
  content = armyUnlocksUi
  id = "SQUADS"
  camera = "researches"
  addChild = function() {
    let mkNotifier = curSection.value != "SQUADS" && hasUnopenedArmyProgress.value
      ? mkNotifierBlink
      : mkNotifierNoBlink
    return {
      watch = [curSection, hasLevelDiscount, curLevelDiscount,
        hasUnseenArmyProgress, hasUnopenedArmyProgress]
      hplace = ALIGN_RIGHT
      pos = [0, hdpx(30)]
      children = hasLevelDiscount.value ? mkNotifier(loc("shop/discount",
          { percents = curLevelDiscount.value }), {}, discountBg)
        : hasUnseenArmyProgress.value ? mkNotifier(loc("hint/takeReward"))
        : null
    }
  }
  onExitCb = function() {
    let armyId = curArmyData.value?.guid ?? ""
    let { unseen = {}, unopened = {} } = seenArmyProgress.value
    if (armyId in unopened)
      markOpened(armyId, unopened[armyId])

    if (armyId not in unseen)
      return true

    let unlock = nextTutorialUnlock.value
    if (unlock != null) {
      showGetUnlockTutorial(unlock)
      return false
    }

    return true
  }
}



let sections = []

sections.append({
  locId = isNewDesign.value ? "menu/battles" : "menu/soldier"
  content = mainScreenUi
  id = mainSectionId
  camera = "soldiers"
})

sections.append(isNewDesign.value
  ? {
      locId = "menu/squads"
      descId = "menu/quartersDesc"
      content = squadSoldiersUi
      id = "SQUAD_SOLDIERS"
      camera = "soldiers_quarters"
    }
  : campaignTabData
)

if (!isNewDesign.value)
  sections.append({
    locId = "menu/researches"
    descId = "menu/researchesDesc"
    content = researchesUi
    id = "RESEARCHES"
    camera = "researches"
    addChild = researchesAlertUi
    onExitCb = function() {
      let armyId = curArmyData.value?.guid
      let unopened = seenResearches.value?.unopened[armyId] ?? {}
      if (unopened.len() > 0)
        markSeen(armyId, unopened.keys(), true)
      return true
    }
  })


sections.append({
  locId = isNewDesign.value ? "menu/shop" : "menu/enlistedShop"
  content = shopUi
  id = "SHOP"
  camera = "researches"
  addChild = shopAlertUi
  onExitCb = function() {
    if (!isNewDesign.value)
      markShopItemOpened(curArmyData.value?.guid, notOpenedShopItems.value)
    return true
  }
  animations = !isNewDesign.value ? null
    : [{ prop = AnimProp.color, from = defTxtColor, to = accentColor, duration = 3,
        loop = true, play = true, easing = CosineFull }]
})

if (isNewDesign.value)
  sections.append({
    locId = "menu/progress"
    content = armyUnlocksUi
    id = "ARMY_PROGRESS"
    camera = "researches"
  })


if (getStoreUrl() != null)
  sections.append({
    locId = "menu/store"
    id = "STORE"
    selectable = false
    onClickCb = @() openUrl(getStoreUrl())
  })

if (getEventUrl() != null)
  sections.append({
    locId = "menu/event"
    id = "EVENT"
    selectable = false
    onClickCb = function(){
      openUrl(getEventUrl())
      markEventSeen()
    }
    unseenWatch = isEventUnseen
  })

setSectionsSorted(sections)
